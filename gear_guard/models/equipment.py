from odoo import models, fields, api

class GearGuardCategory(models.Model):
    _name = 'gearguard.equipment'
    _description = 'Equipment Category'
    
    name = fields.Char(string='Category Name', required=True)

class GearGuardEquipment(models.Model):
    _name = 'gearguard.equipment'
    _description = 'Equipment Asset'
    _inherit = ['mail.thread']

    name = fields.Char(string='Equipment Name', required=True)
    serial_no = fields.Char(string='Serial Number', required=True)
    category_id = fields.Many2one('gearguard.category', string='Category')
    
    purchase_date = fields.Date(string='Purchase Date')
    warranty_info = fields.Text(string='Warranty Information')
    location = fields.Char(string='Location')
    
    # Ownership
    department = fields.Char(string='Department')
    employee_id = fields.Many2one('res.users', string='Assigned Employee')
    
    # Maintenance Defaults
    team_id = fields.Many2one('gearguard.team', string='Maintenance Team')
    technician_id = fields.Many2one('res.users', string='Default Technician')
    
    is_usable = fields.Boolean(string='Is Usable', default=True, tracking=True)
    maintenance_count = fields.Integer(compute='_compute_maintenance_count', string='Maintenance Count')

    def _compute_maintenance_count(self):
        for record in self:
            # Count only active requests (not Repaired or Scrap)
            record.maintenance_count = self.env['gearguard.request'].search_count([
                ('equipment_id', '=', record.id),
                ('stage', 'not in', ['repaired', 'scrap'])
            ])

    def action_view_maintenance_requests(self):
        """ Smart button action to view related requests """
        return {
            'name': 'Maintenance Requests',
            'type': 'ir.actions.act_window',
            'res_model': 'gearguard.request',
            'view_mode': 'tree,form,kanban',
            'domain': [('equipment_id', '=', self.id)],
            'context': {'default_equipment_id': self.id},
        }