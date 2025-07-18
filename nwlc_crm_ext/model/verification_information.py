from odoo import api , fields , models
from odoo.exceptions import UserError




class LeadVerificationLine(models.Model):
    _name = 'lead.verification.line'
    _description = 'Verification Information Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    lead_id = fields.Many2one('crm.lead', string="Lead")
    name = fields.Char(string="Name")
    credit_check_date = fields.Date(string="Credit Check Date",tracking = True)
    new_credit_score = fields.Integer(string="New Credit Score",tracking = True)
    need_cr_check = fields.Boolean(string="Need CR Check",tracking = True)
    verified = fields.Boolean(string="Verified",tracking = True)
    discrepancy = fields.Boolean(string="Discrepancy",tracking = True)
    discrepancy_loan_amt = fields.Integer(string="Discrepancy Loan Amt",tracking = True)
    discrepancy_reason = fields.Selection(
        [
            ('none','None'),
            ('collection_to_loan_amount','Collection To Loan Amount'),
            ('took_loan','Took Loan'),
            ('took_2nd_loan','Took 2nd Loan'),
            ('increased_original_amount','Increased Original Amount')
        ],string="Discrepancy Reason",
        tracking = True
    )
    discrepancy_status = fields.Selection(
        [
            ('none','None'),
            ('open','Open'),
            ('closed_not_playing','Closed Not Playing'),
            ('closed_no_response','Closed No Response'),
            ('closed_won','Closed Won'),
            ('sent_dispute_email','Sent Dispute Email'),
            ('sent_to_legal','Sent To Legal'),
            ('closed_verified','Closed Verified'),
            ('closed_won_payments','Closed Won Payments')
        ],string="Discrepancy Status",
        tracking = True
    )
    discrepancy_loan_date = fields.Date(string="Discrepancy Loan Date",tracking = True)
    discrepancy_lender = fields.Char(string="Discrepancy Lender",tracking = True)
    potential_fee_due = fields.Integer(string="Potential Fee Due",tracking = True)
    mgr_reviewed = fields.Boolean(string="MGR Reviewed",tracking = True)
    new_fee_collected_date = fields.Date(string="New Fee Collected Date",tracking = True)
    processor_audit = fields.Selection(
        [
            ('no_final_email','No Final Email'),
            ('no_loan_savings','No Loan Savings'),
            ('no_biz_loan_options','No Biz Loan Options'),
            ('no_personal_loan_options','No Personal Loan Options'),
            ('missing_lender','Missing Lender'),
            ('closed_incorrectly_notes','Closed Incorrectly(Notes)'),
            ('send_to_drp','Send to DRP'),
            ('send_to_ertc','Send to ERTC'),
            ('send_to_ca_mortgage','Send to CA Mortgage'),
            ('incorrect_dead_sales_reason','Incorrect Dead Sales Reason'),
            ('missing_emails','Missing Email(s)'),
            ('see_mgr','See MGR'),
            ('missing_generated_email','Missing Generated email'),
            ('password_incorrect_format','Password incorrect format'),
            ('missing_income_household','Missing Income/ Household'),
            ('missing_loan_amount','Missing/Wrong Loan amount'),
            ('missing_ja_income','Missing JA Income'),
            ('wrong_stage','Wrong Stage'),
            ('missing_info','Missing Info'),
            ('incorrect_lender','Incorrect Lender')
        ],
        string="Processor Audit",
        tracking = True
    )
    apps_error = fields.Selection(
        [
            ('missing_ss','Missing/wrong screenshot'),
            ('no_max_amount','No Max amount'),
            ('not_using_personal_email','Not using personal e-mail'),
            ('didnt_select_offer','Didnt select offer on LQ/Upstart'),
            ('didnt_verify_cr','Didnt verify CR for existing loans'),
            ('closed_incorrectly','Closed Incorrectly'),
            ('application_typo','Application Typo'),
            ('applied_wrong_amount','Applied wrong amount'),
            ('Wrong_status','Wrong status'),
            ('wrong_lender_info','Wrong lender Info'),
            ('did_not_follow_apps_rules','Did not follow apps rules'),
            ('incomplete_cr_detail','Incomplete CR Detail'),
            ('wrong_cr_detail','Wrong CR detail'),
            ('wrong_client_info_used','Wrong client info used')
        ],
        string="Apps Error",
        tracking = True
    )
    new_amt_collected = fields.Integer(string="New Amt Collected",tracking = True)
    added_lender_error = fields.Selection(
        [
            ('missing_ss_no_max_amount','Missing/wrong screenshot No Max amount'),
            ('not_using_personal_email','Not using personal e-mail'),
            ('didnt_select_offer','Didnt select offer on LQ/Upstart'),
            ('didnt_veriy_cr','Didnt verify CR for existing loans'),
            ('closed_incorrectly','Closed Incorrectly'),
            ('application_typo','Application Typo'),
            ('applied_wrong_amount','Applied wrong amount')
        ],
        string="Added Lender Error",
        tracking = True
    )
    sales_error = fields.Selection(
        [
            ('blank','Blank'),
            ('missing_wrong_income','Missing/wrong Income'),
            ('typo','Typo'),
            ('missing_mtg_rent','Missing MTG/ Rent'),
            ('missing_college_info','Missing College info'),
            ('wrong_info','Wrong Info'),
            ('missing_wrong_employer_info','Missing/wrong Employer info'),
            ('no_ssn','No SSN'),
            ('missing_wrong_employer_info','Missing/wrong Retired info'),
            ('converted_incorrectly','Converted Incorrectly'),
            ('csa_not_signed','CSA not signed'),
            ('missing_cr_wrong_cr','Missing CR/Wrong CR')
        ],
        string="Sales Error",
        tracking = True
    )
    to_call = fields.Boolean(string="To Call",tracking = True)
    shark_tank = fields.Boolean(string="Shark Tank",tracking = True)
    apps_audit = fields.Boolean(string="APPS AUDIT",tracking = True)