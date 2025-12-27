from odoo import models, fields

class GearGuardEquipment(models.Model):
    _name = 'gear_guard.equipment'
    _description = 'Equipment'

    name = fields.Char(string='Equipment Name', required=True)
    serial_number = fields.Char(string='Serial Number')
    purchase_date = fields.Date(string='Purchase Date')
    warranty_date = fields.Date(string='Warranty Expiry')

    department_id = fields.Many2one('hr.department', string='Department')
    employee_id = fields.Many2one('hr.employee', string='Assigned Employee')

    maintenance_team_id = fields.Many2one(
        'gear_guard.maintenance.team',
        string='Maintenance Team',
        required=True
    )

    location = fields.Char(string='Location')
    active = fields.Boolean(default=True)