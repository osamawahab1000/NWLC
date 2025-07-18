# -*- coding: utf-8 -*-
{
    'name': "Portal CRM custom",
    'summary': "portal crm.",

    'description': """
        
    """,

    "author": "Raheel Aslam",
    'license': 'OPL-1',
    'version': '18.0',
    "category": 'crm',
    "currency": 'USD',
    "support": 'raheelsalam95@gmail.com',

    'depends': ['base', 'portal', 'crm', 'stock', 'sale', 'mail'],

    'data': [
        'views/crm_portal_template.xml',
        'views/res_users.xml',
    ],


    'application': True,
    'installable': True,
    'auto_install': False,
}
