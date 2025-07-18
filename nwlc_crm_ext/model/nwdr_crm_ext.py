from odoo import api , fields , models
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit="res.company"

    is_nwdr = fields.Boolean(string="Is NWDR")


 

NWDR_LEAD_STATE = [
    ('lead','Lead'),
    ('duplicate','Duplicate'),
    ('client_fdr','Client FDR'),
    ('client_css','Client CSS'),
    ('client_contact_made','Client Contact Made'),
    ('do_not_call','Do Not Call'),
    ('client_requested_to_be','Client Requested To Be'),
    ('fl_loan_funded','FL Loan Funded'),
    ('f+_loan_funded','F+ Loan Funded'),
    ('tbc_loan_funded','TBC Loan Funded'),
    ('training_file','Training File'),
    ('unable_to_service','Unable To Service')
] 

class CRMLead(models.Model):
    _inherit="crm.lead"
    



    nwdr_lead_state = fields.Selection(
        selection=NWDR_LEAD_STATE,
        string="Status", 
        copy=False,
        default="lead",
        readonly=False
    )
    company_name = fields.Many2one('res.company', string="Company Name",domain=[('id', 'in', [1, 3])])
    company_id_new = fields.Many2one('res.company',default=lambda self: self.env.company.id,)
    nwdr = fields.Boolean(string="NWDR",  related="company_id_new.is_nwdr")
    owner = fields.Selection(
        [
            ('angela','Angela '),
            ('sebastian','Sebastian'),
            ('jenifer','Jenifer '),
            ('alan','Alan ')
        ],
        strings="Owner",
        tracking= True
    )
    lead_type = fields.Selection(
        [
            ('purl_form','Purl Form'),
            ('nwdr_purl','NWDR Purl'),
            ('nwdr_live_call','NWDR Live Call'),
            ('the_borrowing_club_loan_turn_down_tive_transfer','The Borrowing Club Loan Turn Down Live Transfer'),
            ('the_borrowing_club_loan_turn_down_emailed_submission','The Borrowing Club Loan Turn Down Emailed Submission'),
            ('loanQuo_shark_tank_submission','LoanQuo Shark Tank Submission'),
            ('nwdr_shark_tank_submission','NWDR Shark Tank Submission'),
            ('work_the_Lead_call_center_lead','Work the Lead call center lead'),
            ('loan_offer_response_live_call','LOAN OFFER RESPONSE LIVE CALL'),
            ('nationwide_loan_turndown','Nationwide loan Turndown'),
            ('nationwide_live_transfer','Nationwide Live Transfer'),
            ('client_referral','Client Referral')
        ],
        string="Lead Type", 
        tracking= True
    )
    access_code = fields.Char(string="Access Code", tracking= True)
    lead_phase = fields.Selection(
        [
            ('phase_i','Phase I - Trying to Contact'),
            ('phase_ia','Phase I(a) - Initial Contact Made with client via phone or email'),
            ('phase_iii','Phase III - Statements Received/CR Pulled Building File'),
            ('phase_iiia','Phase III(a)- Full app taken unable to reach client for proposal Phase IV(a)- Proposal Sent/Waiting on decision'),
            ('phase_ivb','Phase IV(b)- Proposal Sent/Hot prospect ready to go'),
            ('phase_ivc','Phase IV(c)- Proposal Sent/ Client Declined Program'),
            ('phase_ivd','Phase IV(d)- F+ Link sent client approved/Waiting on Decision'),
            ('phase_ive','Phase IV(e)- FL submission/ Waiting on results to follow'),
            ('phase_ivg','Phase IV(g)- Business Loan Submission/ Waiting on results to follow up'),
            ('phase_ivh','Phase IV(H)- Less than $7500 in Debt/DQ for loan/Recent BK'),
            ('phase_ivi','Phase IV(I)- Proposal Sent/CA Resident - Docs out'),
            ('phase_va','Phase V (A) - Contract Out'),
            ('phase_vb','Phase V (b)- Contract Received'),
            ('phase_vi','Phase VI - Welcome Call Completed/Enrolled'),
            ('phase_vii','Phase VII - Welcome Call Completed-Client terminated before 1st payment')
        ],string="Lead Phase", 
        tracking= True
    )
    lead_name = fields.Char(string="Lead Name", tracking= True)
    # phone = fields.Integer(string="Phone")
    # mobile = fields.Integer(string="Mobile")
    email = fields.Char(string="Email", tracking= True)
    affiliate = fields.Char(string="Affiliate", tracking= True)
    source = fields.Char(string="Source", tracking= True)
    


    def action_send_to_tbc(self):
        """Empty function for button action."""
        # Currently, this function does nothing.
        return True
    
    
    def action_send_to_cap(self):
        """Empty function for button action."""
        # Currently, this function does nothing.
        return True
    

    def action_send_old_fa(self):
        """Empty function for button action."""
        # Currently, this function does nothing.
        return True


    def action_send_to_nwlc(self):
        """Empty function for button action."""
        # Currently, this function does nothing.
        return True


    # company_id = fields.Many2one('res.company', string="Company", compute="_compute_specific_company")

    # @api.depends('company_id')
    # def _compute_specific_company(self):
    #     specific_company = self.env['res.company'].browse(self.env.user.company_id.id)
    #     for record in self:
    #         if specific_company.exists():
    #             record.company_id = specific_company
    
    @api.depends()
    def compute_nwdr(self):
        for rec in self:
            company =  self.env['res.company'].search([('id','=',self.env.user.company_id.id)])
            raise UserError(company)
            if company.is_nwdr:
                rec['nwdr'] = True



    """
    DETAILS TAB Fields On NWDR Leads Form 
        Author : Wasif
    """


    """
    PRIMARY APPLICANT INFO Fields On NWDR Leads Form 
        Author : Wasif
    """



    primary_first_name = fields.Char(string="Primary First Name", tracking= True)
    last_name = fields.Char(string="Last Name", tracking= True)
    spanish_speaking = fields.Boolean(string="Spanish Speaking", tracking= True)
    social_security_number = fields.Char(string="Social Security Number", tracking= True)
    current_behind_payments = fields.Selection(
        [
            ('current','Current'),
            ('behind','Behind')
        ],string="Current or behind on  Payments", 
        tracking= True
    )            
    currently_enrolled_in_nwdr = fields.Char(string="Currently enrolled in NWDR or filed BK in last 3 years", tracking= True)
    currency_id = fields.Many2one('res.currency', string="Currency", tracking= True)
    amount_owed = fields.Monetary(string="Amount Owed", currency_field='currency_id', tracking= True)
    street = fields.Char(string="Street", tracking= True)
    hardship_details = fields.Text(string="Hardship Details", tracking= True)
    city = fields.Char(string="City", tracking= True)
    state = fields.Char(string="State", tracking= True)
    date_of_birth = fields.Date(string="Date Of Birth", tracking= True)
    marital_status = fields.Selection(
            [
                ('single','Single'),
                ('married','Married'),
                ('divorced','Divorced')
            ],
            string="Marital Status", 
            tracking= True
    )
    gender = fields.Selection(
        [
            ('male','Male'),
            ('female','Female'),
        ],
        string="Gender", 
        tracking= True
    )
    postal_code = fields.Char(string="Postal Code", tracking= True)
    savings_account = fields.Char(string="Savings Account", tracking= True)



    """
    SYSTEM INFORMATION Fields On NWDR Leads Form 
        Author : Wasif
    """


    created_by = fields.Char(string="Created By", tracking= True)
    # last_modified_by = fields.Char("ir.models.fields.write_uid", string="Last Modified By")
    last_seen_by = fields.Char(string="Last Seen By", tracking= True)
    next_activity_by = fields.Char(string="Next Activity By", tracking= True)
    last_activity_by = fields.Char(string="Last Activity By", tracking= True)
    owner_last_modified_by = fields.Char(string="Owner Last Modified By", tracking= True)
    timestamp_dead_decline_reason = fields.Char(string="Timestamp: Dead - Declined Reason", tracking= True)
    date_created = fields.Date(string="Date Created", tracking= True)
    date_last_modified = fields.Date(string="Date Last Modified", tracking= True)
    date_last_seen = fields.Date(string="Date Last Seen", tracking= True)
    date_next_activity = fields.Date(string="Date Next Activity", tracking= True)
    date_last_activity = fields.Date(string="Date Last Activity", tracking= True)
    owner_last_modified = fields.Date(string="Owner Last Modified", tracking= True)
    sales_error_audit = fields.Selection(
        [
            ('blank', 'Blank'),
            ('lead_not_worked', 'Lead Not Worked'),
            ('candidate_for_business_loan', 'Candidate For Business Loan'),
            ('candidate_for_drp', 'Candidate For DRP'),
            ('candidate_for_ca_mtg', 'Candidate For CA MTG/ERTC'),
            ('closed_incorrectly', 'Closed Incorrectly'),
            ('missing_info', 'Missing Info')
        ],
        string="SALES ERROR/AUDIT", 
        tracking= True
    )
    csa_signed = fields.Boolean(string="CSA Signed", tracking= True)





    """
        JA PERSONAL INFO Fields On NWDR Leads Form 
            Author : Wasif
    """



    ja_first_name = fields.Char(string="JA First Name", tracking= True)
    ja_middle_name = fields.Char(string="JA Middle Name", tracking= True)
    ja_last_name = fields.Char(string="JA Last Name", tracking= True)
    ja_date_of_birth = fields.Date(string="JA Date Of Birth", tracking= True)
    ja_social_security_number = fields.Char(string="JA Social Security Number", tracking= True)



    """
        LOAN APPLICATION Fields On NWDR Leads Form 
            Author : Wasif
    """




    profession = fields.Char(string="Profession", tracking= True)
    employed = fields.Selection(
        [
            ('employed','Employed'),
            ('self_employed','Self Employed'),
            ('retired','Retired/Fixed Income'),
            ('unemployed','Unemployed')
        ],string="Employed/Self Employed", 
        tracking= True
    )
    monthly_income = fields.Monetary(string="Monthly Income", currency_field='currency_id', tracking= True)
    net_income = fields.Monetary(string="Net Income", currency_field='currency_id', tracking= True)
    requested_loan_amount = fields.Monetary(string="Requested Loan Amount", currency_field='currency_id', tracking= True)
    bank_relationship = fields.Text(string="Bank Relationship", tracking= True)
    credit_store = fields.Integer(string="Credit Score", tracking= True)
    application_stage = fields.Char(string="Application Stage", tracking= True)
    application_status = fields.Char(string="Application Status", tracking= True)
    reject_reason = fields.Char(string="Reject Reason", tracking= True)
    loan_offer_status = fields.Selection(
        [
            ('',''),
            ('',''),
        ],string="Loan Offer Status", tracking= True
    )





    """
    CLIENT FINANCIAL DATA Fields On NWDR Leads Form 
        Author : Wasif
    """


    document = fields.Selection(
        [
            ('yes','Yes'),
            ('no','No')
        ],string="1099 Documents", 
        tracking= True
    )
    total_unsecured_debt = fields.Monetary(string="Total Unsecured Debt", currency_field='currency_id', tracking= True)
    total_unsecured_debt_payment = fields.Monetary(string="Total Unsecured Debt Payment", currency_field='currency_id', tracking= True)
    total_monthly_expenses = fields.Monetary(string="Total Monthly Expenses on Credit Report", currency_field='currency_id', tracking= True)
    debt_to_income_ratio = fields.Float(string="Debt Tp Income Ratio", tracking= True)
    bankruptcy = fields.Selection(
        [
            ('more_than_years_ago','More than 3 years ago'),
            ('never','Never'),
            ('within_Last_years','Within Last 3 years')
        ],string="Bankruptcy", 
        tracking= True
    )
    mortgage_amount_owed = fields.Monetary(string="Mortgage Amount Owed", currency_field='currency_id', tracking= True)
    mortgage_tradeline_age = fields.Char(string="1st Mortgage Tradeline Age", tracking= True)
    mortgage_history = fields.Selection(
        [
            ('late_prior_months','Late Prior to 12 Months'),
            ('late_within_months','Late within Last 12 Months'),
            ('no_late_payments','No Late Payments')
        ],string="1st Mortgage History", 
        tracking= True
    )
    score_models = fields.Text(string="Score Models", tracking= True)
    revolving_credit_utilization = fields.Float(string="Revolving Credit Utilization", tracking= True)


    """
    Financial Analysis Fields On NWDR Leads Form 
        Author : Wasif
    """
    
    monthly_payment = fields.Monetary(string="Monthly Payment", currency_field='currency_id', tracking= True)
    minimum_payment = fields.Monetary(string="Minimum Payment", currency_field='currency_id', tracking= True)
    payoff_time = fields.Integer(string="Payoff Time", tracking= True)
    payoff_time_two = fields.Integer(string="Payoff Time #2", tracking= True)
    payoff_time_three = fields.Integer(string="Payoff Time #3", tracking= True)
    payoff_time_four = fields.Integer(string="Payoff Time #4", tracking= True)
    min_payment = fields.Monetary(string="Min Payment %", currency_field='currency_id', tracking= True)
    national_cc = fields.Integer(string="National CC", tracking= True)
    current_debt = fields.Monetary(string="Current Debt", currency_field='currency_id', tracking= True) 
    interest_cost = fields.Monetary(string="Interest Cost", currency_field='currency_id', tracking= True)
    interest = fields.Char(string="Interest", tracking= True) 
    total_cost = fields.Monetary(string="Total Cost", currency_field='currency_id', tracking= True) 
    remaining_balance = fields.Monetary(string="Remaining Balance", currency_field='currency_id', tracking= True) 
    consolidated_payment_two = fields.Monetary(string="Consolidated Payment #2", currency_field='currency_id', tracking= True)
    consolidated_payment_three = fields.Monetary(string="Consolidated Payment #3", currency_field='currency_id', tracking= True)
    consolidated_payment_four = fields.Monetary(string="Consolidated Payment #4", currency_field='currency_id', tracking= True)