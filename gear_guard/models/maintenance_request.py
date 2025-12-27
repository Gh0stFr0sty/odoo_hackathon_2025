from odoo import models, fields, api
from odoo.exceptions import UserError

class GearGuardMaintenanceRequest(models.Model):
    _name = 'gear_guard.maintenance.request'
    _description = 'Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Subject', required=True, tracking=True)

    equipment_id = fields.Many2one(
        'gear_guard.equipment',
        string='Equipment',
        required=True,
        tracking=True
    )

    maintenance_team_id = fields.Many2one(
        'gear_guard.maintenance.team',
        string='Maintenance Team',
        tracking=True
    )

    technician_id = fields.Many2one(
        'res.users',
        string='Assigned Technician',
        tracking=True
    )

    request_type = fields.Selection(
        [
            ('corrective', 'Corrective'),
            ('preventive', 'Preventive')
        ],
        string='Request Type',
        required=True,
        default='corrective',
        tracking=True
    )

    scheduled_date = fields.Datetime(string='Scheduled Date')
    duration = fields.Float(string='Duration (Hours)')

    state = fields.Selection(
        [
            ('new', 'New'),
            ('in_progress', 'In Progress'),
            ('repaired', 'Repaired'),
            ('scrap', 'Scrap')
        ],
        string='Status',
        default='new',
        tracking=True
    )

@api.onchange('equipment_id')
def _onchange_equipment_id(self):
    if self.equipment_id:
        self.maintenance_team_id = self.equipment_id.maintenance_team_id
