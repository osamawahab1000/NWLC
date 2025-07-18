# -*- coding: utf-8 -*-

{
    "name": "CRM Kanban Company Stages",
    "author": "Raheel Aslam",
    "website": "https://softapex.odoo.com/",
    "support": "raheelaslam95@gmail.com",
    "version": "18.0",
    "license": "OPL-1",
    "category": "Extra Tools",
    "summary": "CRM lead kanban stages visibility w.r.t company",
    "description": """CRM lead kanban stages visibility w.r.t company.""",
    "depends": ["base", "web", "crm" ],
    "data": [
        "views/crm_stage.xml",
        "views/crm_lead.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'crm_kanban_company_stages/static/src/views/**/*',
        ],
    },
    "auto_install": False,
    "installable": True,
    "application": True,
}
