{
    'name': 'GearGuard - Maintenance Tracker',
    'version': '1.0',
    'summary': 'Asset and maintenance management module',
    'description': 'Odoo Hackathon project - GearGuard',
    'author': 'Odoo Hackathon Team',
    'category': 'Operations',
    'depends': ['base', 'mail'],
    'data': [
    'views/equipment_views.xml',
    'views/maintenance_team_views.xml',      # defines action_gearguard_team
    'views/maintenance_request_views.xml',
    'views/gearguard_menus.xml',              # menus come LAST
    ],
    'application': True,
}