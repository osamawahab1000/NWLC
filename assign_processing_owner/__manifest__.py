# -*- coding: utf-8 -*-
{
    'name': "Assign Processing Owner",
    'version': '18.0',
    'category': 'CRM',
    'summary': """
        Module To Assign Processing Owner to multiple leads from wizard.
        """,
    'description': """
       CRM Lead
       Crm
       Lead
       Assign
       Processing Owner
       Processing Owner Assign
       Assign Processing Owner
    """,
    'author': "Wasif Hassan",
    'company': '',
    'website': "",
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/assign_processing_owner_wizard.xml',
    ],
   
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
