from odoo import models, fields

class GearGuardCategory(models.Model):
    _name = 'gearguard.category'
    _description = 'Equipment Category'

    name = fields.Char(required=True)
    description = fields.Text()