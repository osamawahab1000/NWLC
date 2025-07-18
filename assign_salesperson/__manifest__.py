# -*- coding: utf-8 -*-
{
    'name': "Assign Salesperson",
    'version': '18.0',
    'category': 'CRM',
    'summary': """
        Module To Assign Salesperson to multiple leads from wizard.
        """,
    'description': """
       CRM Lead
       Crm
       Lead
       Assign
       Salesperson
       Salesperson Assign
       Assign Salesperson
    """,
    'author': "Muhammad Bilal",
    'company': '',
    'website': "",
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/assign_salesperson_wizard.xml',
    ],
   
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
