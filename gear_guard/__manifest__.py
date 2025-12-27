{
    'name': 'GearGuard - Maintenance Tracker',
    'version': '1.0',
    'summary': 'Asset and maintenance management module',
    'description': 'Odoo Hackathon project - GearGuard',
    'author': 'Odoo Hackathon Team',
    'category': 'Operations',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/equipment_views.xml',
        'views/maintenance_team_views.xml',
        'views/maintenance_request_views.xml',
        'views/menu_items.xml',
    ],
    'application': True,
}