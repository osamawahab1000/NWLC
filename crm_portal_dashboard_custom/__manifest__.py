# -*- coding: utf-8 -*-
{
    'name': "Portal CRM custom Dashboard",
    'summary': "",

    'description': """
        
    """,

    "author": "Muhammad Bilal",
    'license': 'OPL-1',
    'version': '17.0',
    "category": 'crm',
    "currency": '',
    "support": 'bilalsaylani451@gmail.com',

    'depends': ['base', 'portal', 'crm', 'stock', 'sale', 'mail'],

    'data': [
        'views/portal_dashboard_view.xml',
    ],


    'assets': {

        'web.assets_backend': [
           
        ],
    },

    'application': True,
    'installable': True,
    'auto_install': False,
}
