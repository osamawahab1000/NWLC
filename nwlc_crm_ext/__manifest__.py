# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'NWLC Crm Ext',
    'version': '1.2',  
    'category': 'CRM',
    'sequence' : -1,
    'summary': 'CRM Leads',
    'description': """""",
    'depends': ['base','crm','base_setup'],
    'demo': [],
    'data':[
        'security/ir.model.access.csv',
        'security/nwlc_record_rules.xml',
        'views/dead_sale.xml',
        'views/app_specialist.xml',
        'views/res_company.xml',
        'views/lenders.xml',
        'views/lender_line.xml',
        'views/creditors.xml',
        'views/creditors_status.xml',
        'views/industry.xml',
        'views/dead_reason.xml',
        'views/object_reason.xml',
        'views/flags_lead.xml',
        'views/script.xml',
        'views/transferred_out_reason.xml',
        'views/best_contact_time.xml',
        'views/affiliate_partner.xml',
        'views/crm_ext.xml',
        'views/credit_card_form_wizard.xml',
        'views/ach_form_wizard.xml',
        'views/fa_template_wizard.xml',
        'views/csa_general_wizard.xml',
        'views/business_general_agreement_wizard.xml',
        'views/spanish_csa_rev_wizard.xml',
        'views/lead_stage_views.xml',
        'views/discrepancy_view.xml',
        'views/crm_stage.xml',
        'views/dead_reason_wizard.xml',
        'views/crm_team_inherited.xml',
        'views/affiliate_api_access.xml',
        # email template
        'data/csa_email_template.xml',
        'data/paperformat_data.xml',
        'data/affiliate_sequence.xml',
        'report/csa_general_agreement_report.xml',
        'report/csa_general_agreement.xml',
        'report/spanish_csa_rev.xml',
        'report/ach_form.xml',
        'report/fa_template.xml',
        'report/business_general_agreement.xml',
        'report/credit_card_form.xml',
        'views/crm_ext_kanban_view.xml',
        # workflows Email templates
        'data/workflows_template.xml',
        # Wizard views
        'wizard/stage_wizard.xml'
        

    ],

   'assets': {
        'web.assets_backend': [
            'nwlc_crm_ext/static/src/js/lead_statusbar.js',
            # 'nwlc_crm_ext/static/description/header_ach_form.png',
            # 'nwlc_crm_ext/static/src/img/visa_credit.jpg',
            # 'nwlc_crm_ext/static/src/img/master_card.jpg',
        ]
    },
    'application':True,
    'installable': True,
    'auto_install':False,
    'license': 'LGPL-3',
}
