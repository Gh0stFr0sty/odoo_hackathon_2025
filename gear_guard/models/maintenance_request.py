from odoo import models, fields, api
from datetime import date

class GearGuardRequest(models.Model):
    _name = 'gearguard.request'
    _description = 'Maintenance Request'
    _inherit = ['mail.thread']

    subject = fields.Char(string='Subject', required=True)
    description = fields.Text(string='Description')
    
    # Request Details
    request_type = fields.Selection([
        ('corrective', 'Corrective (Breakdown)'),
        ('preventive', 'Preventive (Routine Checkup)')
    ], string='Request Type', default='corrective', required=True)
    
    equipment_id = fields.Many2one('gearguard.equipment', string='Equipment', required=True)
    category_id = fields.Many2one('gearguard.category', related='equipment_id.category_id', string='Category', readonly=True, store=True)

    # Workflow
    stage = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('repaired', 'Repaired'),
        ('scrap', 'Scrap')
    ], string='Stage', default='new', group_expand='_read_group_stage_ids', tracking=True)
    
    # Scheduling & Assignment
    scheduled_date = fields.Date(string='Scheduled Date', tracking=True)
    duration = fields.Float(string='Duration (Hours)')
    
    team_id = fields.Many2one('gearguard.team', string='Team', tracking=True)
    # Helper field to filter technicians who belong to the selected team
    team_member_ids = fields.Many2many('res.users', related='team_id.member_ids')
    technician_id = fields.Many2one('res.users', string='Technician', tracking=True)

    is_overdue = fields.Boolean(compute='_compute_is_overdue', string='Overdue')

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """ Ensure all stages are visible in Kanban even if empty """
        return ['new', 'in_progress', 'repaired', 'scrap']

    @api.depends('scheduled_date', 'stage')
    def _compute_is_overdue(self):
        today = date.today()
        for record in self:
            if record.scheduled_date and record.scheduled_date < today and record.stage not in ['repaired', 'scrap']:
                record.is_overdue = True
            else:
                record.is_overdue = False

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        """ Auto-fill logic from """
        if self.equipment_id:
            self.team_id = self.equipment_id.team_id
            self.technician_id = self.equipment_id.technician_id

    def write(self, vals):
        """ Scrap logic from """
        res = super(GearGuardRequest, self).write(vals)
        if 'stage' in vals and vals['stage'] == 'scrap':
            for record in self:
                if record.equipment_id:
                    record.equipment_id.write({'is_usable': False})
                    record.equipment_id.message_post(body="Equipment marked as Unusable because maintenance request was moved to Scrap.")
        return res