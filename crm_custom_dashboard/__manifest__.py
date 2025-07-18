# -*- coding: utf-8 -*-
################################################################################
################################################################################
{
    'name': "Odoo CRM Custom Dashboard",
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': """Odoo Dynamic Dashboard, Dynamic Dashboard, Odoo18, Odoo18 Dashboards, Dashboard with AI, AI Dashboard, Odoo Dashboard,Graph View,""",
    'description': """Create Configurable Odoo Dynamic Dashboard to get the 
    information that are relevant to your business, department, or a specific 
    process or need""",
    'live_test_url': '',
    'author': 'Muhammad Bilal,Wasif Hassan',
    'company': '',
    'maintainer': '',
    'website': "",
    'depends': ['web','crm'],
    'data': [
       'views/dashboard_action.xml',
       'data/paperformat_data.xml',
       'report/report_template.xml',
       'report/report.xml',
       
    ],
    'assets': {
        'web.assets_backend': [
            'crm_custom_dashboard/static/src/js/**/*.js',
            'crm_custom_dashboard/static/src/xml/**/*.xml',
           
        ],
    },
    'images': ['static/description/banner.gif'],
    'license': "AGPL-3",
    'installable': True,
    'auto_install': False,
    'application': True,
}



