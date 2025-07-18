from odoo import api , fields , models,Command,_
from odoo.exceptions import UserError, ValidationError

import requests
import json
import base64
from requests.auth import HTTPBasicAuth
from datetime import datetime
import time

from collections import defaultdict


LEAD_STATE = [
    ('assigned','Assigned'),
    ('1st_day','1st Day'),
    ('2nd_day','2nd Day'),
    ('3rd_day','3rd Day'),
    ('dead','Dead'),
    ('appt','Appt'),
    ('test_lead','Test Lead'),
    ('dnc','DNC'),
    ('transferred_out','Transferred Out')
]
DISPOSITION = [

            ('Disposition', 'Disposition'),
            ('no_answer', 'No Answer'),
            ('dead_air', 'Dead Air'),
            ('quick_hang_up', 'Quick Hang Up'),
            ('invalid_number', 'Invalid Number'),
            ('left_message', 'Left Message'),
            ('wrong_party', 'Wrong Party/Number')
        ]

PROTOCOL = "https"
SANDBOX_HOST = "api-sandbox.stitchcredit.com"
BASE_URL = "/api"
PORT = 443
USERNAME = "jasonm@nationwideloanconsultants.com" 
PASSWORD =  "uKzY5t&rKAVl"

# Pull equifax dep
EQ_SENDBOX_HOST = "api.uat.equifax.com"
EQ_VESION = "v2"
EQ_USERNAME = "4GWwDWGWHSkUfSEdL78QGqd0JmBU69z7"
EQ_PASSWORD = "AoXo5aJkUaTfEkyv"
EQ_HEADERS = {
  'Content-Type': 'application/x-www-form-urlencoded',
}
EQ_PAYLOAD = 'grant_type=client_credentials&scope=https%3A%2F%2Fapi.equifax.com%2Fbusiness%2Foneview%2Fconsumer-credit%2Fv1'

class CRMLead(models.Model):
    _inherit="crm.lead"

    
    """
        Main Fields For Affiliate Leads 
            Author : Wasif
    """

    
    disposition_head = fields.Selection(
        selection=DISPOSITION,
        string="Disposition",
        default="Disposition"
    )
    lead_state = fields.Selection(
        selection=LEAD_STATE,
        string="Status", 
        copy=False,
        default="assigned",
        readonly=False
    )
    probability = fields.Float(string='Probability', default=0.0)
    source_ids = fields.Many2one('affiliate.partner', string='Lead Source', domain="[('affiliate_id', '=', affiliate_name)]",tracking = True)
    affiliate_name = fields.Many2one('affiliate.partner', string='Affiliate Name',tracking = True, domain="[('affiliate_id', '=', False)]")
    affiliate_id = fields.Char(related="affiliate_name.aff_id" , string='Affiliate ID',tracking = True)
    affiliate_email = fields.Char(related="affiliate_name.affiliate_email" , string='Affiliate Email',tracking = True)
    # source = fields.Many2one("res.partner", string="Source")
    # affiliate_name = fields.Many2one("res.partner", string="Affiliate Name")
    affiliate_sales_rep = fields.Char(string="Affiliate Sales Rep",tracking = True)
    # affiliate_lead_id = fields.Integer(string="Affiliate ID")
    processing_owner = fields.Many2one('res.users',string="Processing Owner", tracking= True)

    @api.model
    def check_dead_stage_restriction_js(self, ids):
        for record in self.browse(ids):
            is_owner = record.processing_owner and record.processing_owner.id == self.env.uid
            has_approved_personal = any(
                line.creditor_status_ and line.creditor_status_.name == 'Approved Personal'
                for line in record.lender_line_id
            )
            if is_owner and has_approved_personal:
                raise UserError(
                    "You cannot set this record to 'Dead' while it has a lender with 'Approved Personal' status."
                )
        return True

    second_owner = fields.Many2one('res.users',string="Second Owner", tracking= True)
    live_transfer = fields.Boolean(string="Live Transfer",tracking = True)
    generated_email = fields.Char(string="Generated Email",tracking = True)
    generated_password = fields.Char(string="Generated Password",tracking = True)
    spanish_speaking = fields.Boolean(string="Spanish Speaking",tracking = True)
    requested_loan_amount = fields.Monetary(string="Requested Loan Amount", currency_field='currency_id',tracking = True)
    phone = fields.Char(string="Phone",related="full_name.phone",tracking = True)
    mobile = fields.Char(string="Mobile",related="full_name.mobile",tracking = True)
    application_type = fields.Selection(
        [
            ('individual', 'Individual'),
            ('joint', 'Joint')
        ],
        string="Application Type",
        tracking = True
    )
    loan_type = fields.Selection(
            [
                ('business_loan', 'Business Loan'),
                ('debt_consolidation', 'Debt Consolidation'),
                ('home_improvement', 'Home Improvement/Furnishings'),
                ('other', 'Other'),
                ('personal_business', 'Personal & Business'),
                ('personal_loan', 'Personal Loan'),
                ('sub_prime', 'Sub-Prime')
            ],
            string="Loan Type",
            tracking = True
    )
    email = fields.Char(string="Email",related="full_name.email",tracking = True,readonly=False)
    credit_score = fields.Integer(string="Credit Score",tracking = True)
    client_fee = fields.Monetary(string="Client Fee", currency_field='currency_id',tracking = True)
    employed = fields.Char(string="Employed",tracking = True)
    best_contact_time_id = fields.Many2one("best.contact.time", string="Best Contact Time",tracking = True)
    cc_debt = fields.Char(string="CC Debt",tracking = True)
    primary_gross_annual_income = fields.Monetary(string="Primary Gross Annual Income", currency_field='currency_id',tracking = True)
    currency_id = fields.Many2one('res.currency', string="Currency",tracking = True)
    household_income = fields.Monetary(string="Household Income", currency_field='currency_id',tracking = True)
    verifiable_income_type = fields.Selection(
        [
            ('1099_tax_return', '1099 Tax Return'),
            ('w2_pay_stub', 'W2 Pay Stub'),
            ('alimony_child_support', 'Alimony/Child Support'),
            ('award_letter', 'Award Letter')
        ],
        string="Verifiable Income Type",
        tracking = True
    )
    street = fields.Char(string="string",related="full_name.street")
    street2 = fields.Char(string="string",related="full_name.street2")
    # state_id = fields.Char(string="string",related="full_name.state_id.name")
    city = fields.Char(string="string",related="full_name.city")
    zip = fields.Char(string="string",related="full_name.zip")
    # country_id = fields.Char(string="string",related="full_name.country_id")
    transferred_out_reason_id = fields.Many2one("transferred.out.reason", string="Transferred Out Reason",tracking = True)
    dead_reason_id = fields.Many2one("dead.reason", string="Dead Reason",tracking = True, readonly = True)
    object_reason_id = fields.Many2one("object.reason", string="Objection Reason",tracking = True,readonly = True)
    expedite_file = fields.Boolean(string="Expedite File",tracking = True)
    total_unsecure_debt = fields.Monetary(string="Total Unsecure Debt", currency_field='currency_id',tracking = True)
    total_unsecure_debt_payment = fields.Monetary(string="Total Unsecure Debt Payment", currency_field='currency_id',tracking = True)
    debt_to_income_ratio = fields.Char(string="Debt To Income Ratio", compute="_compute_debt_to_income_ratio",store=True,tracking = True)
    revolving_credit_utilization = fields.Char(string="Revolving Credit Utilization",compute="_compute_utilization_rate",store="True",tracking = True)
    # app_specialist_id = fields.Many2one("app.specialist", string="App Specialist")
    app_specialist = fields.Many2one("res.users",string="App Specialist",tracking = True)
    cr_specialist = fields.Many2one("res.users",string="CR Specialist",tracking = True)
    al_specialist = fields.Many2one("res.users",string="AL Specialist",tracking = True)
    converted_lead = fields.Boolean(string="Lead Converted to Processing")
    converted_lead_date = fields.Datetime(string="Lead Converted Date")
    api_lead = fields.Boolean(string="API")
    # send_fa = fields.Boolean(string="Send FA")

    stage_reason = fields.Selection(
        [
            ('think_about_it', 'Want To Think About It'),
            ('research', 'Do Some Research'),
            ('cannot_sign_csa', 'Cannot sign CSA at the moment'),
            ('setup_call_back', 'Setup call back time'),
            ('could_not_reach', 'Could not reach')
        ],
        string="Stage Reason",
        tracking=True
    )


    
    @api.depends('total_unsecure_debt','primary_gross_annual_income')
    def _compute_debt_to_income_ratio(self):
        for record in self:
            if record.total_unsecure_debt and record.primary_gross_annual_income:
                record.debt_to_income_ratio = (
                    record.total_unsecure_debt / record.primary_gross_annual_income
                ) # Convert ratio to percentage
            else:
                record.debt_to_income_ratio = 0.00

    # bilal add field here 


    lead_stage_id = fields.Many2one(
        'crm.lead.stage', string='Lead Stage', index=True, tracking=True,
        readonly=False, store=True,
        copy=False, group_expand='_read_group_lead_stage_ids', ondelete='restrict',
        )
    

   



    @api.model
    def _read_group_lead_stage_ids(self, leadstages, domain):
        search_domain = []
        # perform search
        stage_ids = leadstages.sudo()._search(search_domain, order=leadstages._order)
        # raise UserError(leadstages.browse(stage_ids))
        return leadstages.browse(stage_ids)
    
    # @api.depends('team_id', 'type')
    # def _compute__lead_stage_id(self):
    #     for lead in self:
    #         if not lead.lead_stage_id:
    #             lead.lead_stage_id = lead._Lead_stage_find(domain=[('fold', '=', False)]).id
    
    # def _Lead_stage_find(self, domain=None, order='sequence, id', limit=1):
    #     """ Determine the stage of the current lead with its teams, the given domain and the given team_id
    #         :param team_id
    #         :param domain : base search domain for stage
    #         :param order : base search order for stage
    #         :param limit : base search limit for stage
    #         :returns crm.stage recordset
    #     """
        
    #     search_domain = [('company_ids', 'in', self.env["res.company"]._company_default_get("crm.lead.stage"))]
    #     return self.env['crm.lead.stage'].search(search_domain, order=order, limit=limit)

    custom_action_name = fields.Char(string="Custom Name", compute="_compute_custom_name")

    @api.depends('state_id', 'company_id')
    def _compute_custom_name(self):
        for record in self:
            prefix = ''
            # Set prefix based on company_id
            if record.company_id.id == 1:
                prefix = 'NWLC '
            elif record.company_id.id == 3:
                prefix = 'TBC '

            # Set name based on state_id
            if record.state_id:
                if record.state_id.code == 'WI':
                    record.custom_action_name = f"{prefix}Spanish CSA Rev(5) WI"
                elif record.state_id.code == 'PA':
                    record.custom_action_name = f"{prefix}Spanish CSA Rev(5) PA"
                elif record.state_id.code == 'NE':
                    record.custom_action_name = f"{prefix}Spanish CSA Rev(5) NE"
                elif record.state_id.code == 'MD':
                    record.custom_action_name = f"{prefix}Spanish CSA Rev(5) MD"
                elif record.state_id.code == 'OK':
                    record.custom_action_name = f"{prefix}Spanish CSA Rev(5) OK"
                elif record.state_id.code == 'WV':
                    record.custom_action_name = f"{prefix}Spanish CSA Rev(5) WV"
                else:
                    record.custom_action_name = f"{prefix}Spanish CSA Rev(5)"
            else:
                record.custom_action_name = f"{prefix}Spanish CSA Rev(5)"

    def write(self, vals):
        for record in self:
            prefix = ''
            # Set prefix based on company_id
            if 'company_id' in vals or record.company_id:
                if vals.get('company_id', record.company_id.id) == 1:
                    prefix = 'NWLC '
                elif vals.get('company_id', record.company_id.id) == 3:
                    prefix = 'TBC '

            if 'state_id' in vals or record.state_id:
                state_code = vals.get('state_id', record.state_id.code)
                if state_code == 'WI':
                    vals['custom_action_name'] = f"{prefix}Spanish CSA Rev(5) WI"
                elif state_code == 'PA':
                    vals['custom_action_name'] = f"{prefix}Spanish CSA Rev(5) PA"
                elif state_code == 'NE':
                    vals['custom_action_name'] = f"{prefix}Spanish CSA Rev(5) NE"
                elif state_code == 'MD':
                    vals['custom_action_name'] = f"{prefix}Spanish CSA Rev(5) MD"
                elif state_code == 'OK':
                    vals['custom_action_name'] = f"{prefix}Spanish CSA Rev(5) OK"
                elif state_code == 'WV':
                    vals['custom_action_name'] = f"{prefix}Spanish CSA Rev(5) WV"
                else:
                    vals['custom_action_name'] = f"{prefix}Spanish CSA Rev(5)"
            else:
                vals['custom_action_name'] = f"{prefix}Spanish CSA Rev(5)"

        return super(CRMLead, self).write(vals)


    custom_action_name_csa = fields.Char(string="Custom Name", compute="_compute_custom_name_csa")

    @api.depends('state_id', 'company_id')
    def _compute_custom_name_csa(self):
        for record in self:
            prefix = ''
            # Set prefix based on company_id
            if record.company_id.id == 1:
                prefix = 'NWLC '
            elif record.company_id.id == 3:
                prefix = 'TBC '

            # Set name based on state_id
            if record.state_id:
                if record.state_id.code == 'WI':
                    record.custom_action_name_csa = f"{prefix}CSA General Agreement WI"
                elif record.state_id.code == 'PA':
                    record.custom_action_name_csa = f"{prefix}CSA General Agreement PA"
                elif record.state_id.code == 'NE':
                    record.custom_action_name_csa = f"{prefix}CSA General Agreement NE"
                elif record.state_id.code == 'MD':
                    record.custom_action_name_csa = f"{prefix}CSA General Agreement MD"
                elif record.state_id.code == 'OK':
                    record.custom_action_name_csa = f"{prefix}CSA General Agreement OK"
                elif record.state_id.code == 'WV':
                    record.custom_action_name_csa = f"{prefix}CSA General Agreement WV"
                else:
                    record.custom_action_name_csa = f"{prefix}CSA General Agreement"
            else:
                record.custom_action_name_csa = f"{prefix}CSA General Agreement"

    def write(self, vals):
        for record in self:
            prefix = ''
            # Set prefix based on company_id
            if 'company_id' in vals or record.company_id:
                if vals.get('company_id', record.company_id.id) == 1:
                    prefix = 'NWLC '
                elif vals.get('company_id', record.company_id.id) == 3:
                    prefix = 'TBC '

            if 'state_id' in vals or record.state_id:
                state_code = vals.get('state_id', record.state_id.code)
                if state_code == 'WI':
                    vals['custom_action_name_csa'] = f"{prefix}CSA General Agreement WI"
                elif state_code == 'PA':
                    vals['custom_action_name_csa'] = f"{prefix}CSA General Agreement PA"
                elif state_code == 'NE':
                    vals['custom_action_name_csa'] = f"{prefix}CSA General Agreement NE"
                elif state_code == 'MD':
                    vals['custom_action_name_csa'] = f"{prefix}CSA General Agreement MD"
                elif state_code == 'OK':
                    vals['custom_action_name_csa'] = f"{prefix}CSA General Agreement OK"
                elif state_code == 'WV':
                    vals['custom_action_name_csa'] = f"{prefix}CSA General Agreement WV"
                else:
                    vals['custom_action_name_csa'] = f"{prefix}CSA General Agreement"
            else:
                vals['custom_action_name_csa'] = f"{prefix}CSA General Agreement"

        return super(CRMLead, self).write(vals)



    def action_send_fa(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'FA Form',
            'res_model': 'fa.template',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_crm_lead_id': self.id,
                'default_full_name': self.full_name.name,
                'default_email': self.email,
                'default_monthly_payment': self.monthly_payment,
                'default_date_sent': self.date_sent,
                # 'default_bank_routing_number': self.bank_routing_number,
                # 'default_bank_account_number': self.bank_account_number,
                # 'default_date_funds_avail': self.date_funds_avail,
                # 'default_account_type': self.account_type,
            },
        }
    
    monthly_payment = fields.Char(string="Amount")
    date_sent = fields.Date(string="Date Sent")

    
    send_to_nwdr = fields.Boolean("Send To Nwdr", default=False)
    def action_send_to_nwdr(self):
        """"""
        # raise UserError("Working")
        for record in self:
            first_stage = self.env['crm.stage'].sudo().search([('company_id','=',4)], order='sequence', limit=1)
            new_lead = record.sudo().copy({
                'company_id': 4,  
                'user_id': record.user_id.id,
                'stage_id':first_stage.id,
                'type':'opportunity',
            })
            if new_lead:
                record.send_to_nwdr = True
                record.message_post(
                    body=f"this Lead is sent to NWDR",
                    subtype_id=self.env.ref('mail.mt_note').id
                )
    
    def action_ach_form(self):
        """Open the ACH Form Wizard."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'ACH Form',
            'res_model': 'ach.form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_crm_lead_id': self.id,
                'default_full_name': self.full_name.name,
                'default_amount': self.amount,
                'default_email': self.email,
                'default_bank_name': self.bank_name,
                'default_bank_routing_number': self.bank_routing_number,
                'default_bank_account_number': self.bank_account_number,
                'default_date_funds_avail': self.date_funds_avail,
                'default_account_type': self.account_type,
            },
        }
    

    
    
    bank_name = fields.Char(string="Bank Name")
    bank_routing_number = fields.Char(string="Bank Routing Number")
    bank_account_number = fields.Char(string="Bank Account Number")
    date_funds_avail = fields.Char(string="Date Funds Available")
    account_type = fields.Selection(
        [
            ('checking','Checking'),
            ('savings','Savings')
        ],string="Account Type"
    )
    
    
    def action_dead_reason_wizard(self):
        """Open the Dead Reason Wizard."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Dead Reason Wizard',
            'res_model': 'dead.reason.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_lead_id': self.id,
                'default_dead_reason_id': self.dead_reason_id,
            },
        }
    
    
    def action_credit_card_form(self):
        """Open the Credit Card Form Wizard."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Credit Card Form',
            'res_model': 'credit.card',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_crm_lead_id': self.id,
                'default_full_name': self.full_name.name,
                'default_email': self.email,
                'default_phone': self.phone,
                'default_street': self.street,
            },
        }
    
    account_type = fields.Selection(
        [
            ('visa','Visa'),
            ('debit','Debit'),
            ('discover','Discover'),
            ('american_express','American Express')
        ],string="Account Type"
    )
    cardholder_name = fields.Char(string="Cardholder Name")
    account_number = fields.Char(string="Account Number")
    exp_date = fields.Date(string="Expiry Date")



    # def send_nwlc_csa_general_spanish(self):
    #     """Placeholder method for the button action."""
    #     return True
    

    # def action_send_nwlc_csa_general(self):
    #     """Placeholder method for the button action."""
    #     self.action_open_csa_general_wizard()
    

    # def action_send_nwlc_business(self):
    #     """Placeholder method for the button action."""
    #     return True
 
    

    

    
    # <subhan >
    is_synced = fields.Boolean(string="Is Synced")
    mirror_id = fields.Integer(string="Mirror Record ID")
    lenders_name_list = fields.Char(string="Lenders")
    is_income_verifiable = fields.Selection(
        [
            ('yes','Yes'),
            ('no','No')
        ],string="Is Income Verifiable"
    )
    no_10 = fields.Char(string="Number 10")
    no_11 = fields.Char(string="Number 11")
    change_fee = fields.Char(string="Change Fee")
    custom_stage_id = fields.Many2one(
        'crm.stage', 
        string='Stage', 
        domain="[('company_id', 'in', [company_id, False])]"
    ) 
    
    stage_id = fields.Many2one(
        'crm.stage', 
        string='Stage', 
        domain="[('company_id', 'in', [company_id, False])]"
    ) 
    
    # @api.depends('lender_line_id')
    def computeLenderName(self):
        for i in self:
            i['lenders_name_list'] = False
            name = ''
            if i.lender_line_id:
                for line in i.lender_line_id:
                    name += str(line.lender_id.name) + ","
                name = name.rstrip(",")
                i['lenders_name_list'] = name
                
    def action_send_survey(self):
        template = self.env['mail.template'].search([('id', '=', 43)], limit=1)
        if template:
            email_values = {
                'email_to': self.full_name.email, 
            }
            template.send_mail(self.id, force_send=True, email_values=email_values)
            
    def send_request(self):
        self.ensure_one()
        template_id = self.env['sign.template'].search([('id','=',3)])
        signers = [{'partner_id': self.full_name.id, 'role_id':1, 'mail_sent_order': 1}]
        # cc_partner_ids = self.cc_partner_ids.ids
        reference = "ACH Form.pdf"
        subject = "Signature Request - ACH Form.pdf"
        sign_request = self.env['sign.request'].create({
            'template_id': template_id.id,
            'request_item_ids': [Command.create({
                'partner_id': signer['partner_id'],
                'role_id': signer['role_id'],
                'mail_sent_order': signer['mail_sent_order'],
            }) for signer in signers],
            'reference': reference,
            'subject': subject,
        })   

    def sendAppliedLenders(self):
        self.computeLenderName()
        template = self.env['mail.template'].search([('id', '=', 35)], limit=1)
        # raise UserError(self.lenders_name_list) 
        if template:
            email_values = {
                'email_to': self.full_name.email, 
            }
            template.send_mail(self.id, force_send=True, email_values=email_values)
            
    def sendAfterConsultation(self):
        self.computeLenderName()
        template = self.env['mail.template'].search([('id', '=', 37)], limit=1)
        if template:
            email_values = {
                'email_to': self.full_name.email, 
            }
            template.send_mail(self.id, force_send=True, email_values=email_values)
    def sendTruthEncloser(self):
        self.computeLenderName()
        template = self.env['mail.template'].search([('id', '=', 36)], limit=1)
        if template:
            email_values = {
                'email_to': self.full_name.email, 
            }
            template.send_mail(self.id, force_send=True, email_values=email_values)
    # </subhan>


    """
        DETAILS TAB Fields On Affiliate Leads Form 
            Author : Wasif
    """
    
    name = fields.Char(string="Name", compute="_compute_name", store=True, readonly=False,tracking = True)
    full_name = fields.Many2one("res.partner", string="Full Name", ondelete="set null")
    first_name = fields.Char(string="First Name",tracking = True)
    last_name = fields.Char(string="Last Name",tracking = True)

    @api.depends('first_name', 'last_name', 'full_name')
    def _compute_name(self):
        """
        Compute the 'name' field based on 'first_name' and 'last_name' or directly from 'full_name'.
        """
        for rec in self:
            if rec.full_name:
                rec.name = rec.full_name.name
            else:
                full_name_str = f"{rec.first_name or ''} {rec.last_name or ''}".strip()
                rec.name = full_name_str or "New Lead"

    def write(self, vals):
        """
        Override the write method to ensure partner is created/linked only on save.
        """
        for rec in self:
        # subhan
            if rec.type == 'lead':
                # raise UserError('working')
                if vals.get('type'):
                    if vals.get('type') == 'opportunity':
                        vals['converted_lead'] = True
                        vals['converted_lead_date'] = datetime.today()
                        if self.env.company.id == 1:
                            if self.loan_type == "sub_prime":
                                vals['stage_id'] = 1
                            else:
                                vals['stage_id'] = 5
                            """Converted lead With Processing Owner Name"""
                            self.send_email_Converted_lead_With_Processing_Owner_Name()
                        if self.env.company.id == 3:
                            if self.loan_type == "sub_prime":
                                vals['stage_id'] = 44
                            else:
                                vals['stage_id'] = 45


        # subhan
            first_name = vals.get('first_name', rec.first_name)
            last_name = vals.get('last_name', rec.last_name)
            full_name_str = f"{first_name or ''} {last_name or ''}".strip()

            if full_name_str and not vals.get('full_name'):
                # Check for an existing partner with the full name
                partner = self.env['res.partner'].search([('name', '=', full_name_str)], limit=1)
                if not partner:
                    # Create the partner if not found
                    partner = self.env['res.partner'].create({
                        'name': full_name_str,
                        'company_id': rec.company_id.id if rec.company_id else False,
                    })
                # Add the partner to vals for updating the full_name field
                vals['full_name'] = partner.id
        return super(CRMLead, self).write(vals)
    
    def send_email_Converted_lead_With_Processing_Owner_Name(self):
        template = self.env.ref('nwlc_crm_ext.email_template_Converted_lead_With_Processing_Owner_Name')  # Replace with your template ID
        if not self.email:
            raise UserError("Customer Email has not provid")
        template.send_mail(
            self.id,  
            force_send=True,  
            email_values={
                'email_to': self.email,
            }
        )

    



    @api.model
    def create(self, vals):
        """
        Override the create method to ensure partner is created/linked when record is saved.
        """
        first_name = vals.get('first_name', '')
        last_name = vals.get('last_name', '')
        full_name_str = f"{first_name or ''} {last_name or ''}".strip()

        if full_name_str and not vals.get('full_name'):
            # Check for an existing partner with the full name
            partner = self.env['res.partner'].search([('name', '=', full_name_str)], limit=1)
            if not partner:
                # Create the partner if not found
                partner = self.env['res.partner'].create({
                    'name': full_name_str,
                    'company_id': vals.get('company_id', False),
                })
            # Link the partner to the full_name field
            vals['full_name'] = partner.id

        return super(CRMLead, self).create(vals)

    @api.onchange('full_name')
    def _onchange_full_name(self):
        """
        Update the 'name' field when a partner is selected from the dropdown.
        """
        for rec in self:
            if rec.full_name:
                rec.name = rec.full_name.name
            else:
                rec.name = "New Lead"

    
    # name = fields.Char(string="Lead Name", compute="_compute_name")
    @api.depends('lead_name','full_name')
    def compute_name(self):
        for rec in self:
            rec['name'] = False
            if rec.full_name:
                rec['name'] = rec.full_name.name
            if rec.lead_name:
                rec['name'] = rec.lead_name
    
    social_security_number = fields.Char(string="Social Security Number",tracking = True)
    # prev_address_street = fields.Char(string="Prev Address Street",tracking = True)
    # prev_state = fields.Many2one("res.country.state", string="Prev State",tracking = True)
    # years_at_previous_address = fields.Char(string="Years At Previous Address",tracking = True)
    personal_banking_info = fields.Char(string="Personal Banking Info",tracking = True)
    how_much_in_liquid_assets = fields.Char(string="How Much In Liquid Assets",tracking = True)
    amount_owed = fields.Monetary(string="Amount Owed", currency_field='currency_id',tracking = True)
    employer_name = fields.Char(string="Employer Name",tracking = True)
    employer_street = fields.Char(string="Employer Street",tracking = True)
    employer_city = fields.Char(string="Employer City",tracking = True)
    month_year_hired = fields.Date(string="Month/Year Hired",tracking = True)
    work_phone = fields.Char(string="Work Phone",tracking = True)
    # prev_job_title = fields.Char(string="Prev Job Title/Position",tracking = True)
    # prev_work_phone = fields.Integer(string="Prev Work Phone",tracking = True)
    debt_relief_solutions = fields.Boolean(string="Debt Relief Solutions",tracking = True)
    date_moved_to_address = fields.Date(string="Date Moved To Address",tracking = True)
    us_citizen = fields.Selection(
        [
            ('yes','Yes'),
            ('no','No')
        ],
        string="U.S Citizen",
        tracking = True
    )
    date_of_birth = fields.Date(string="Date Of Birth",tracking = True)
    # prev_address_city = fields.Char(string="Prev Address City",tracking = True)
    # prev_address_zip = fields.Integer(string="Prev Address Zip",tracking = True)
    marital_status = fields.Selection(
            [
                ('single','Single'),
                ('married','Married'),
                ('divorced','Divorced'),
                ('widowed','Widowed')
            ],
            string="Marital Status",
            tracking = True
    )
    avg_bank_balance = fields.Char(string="Average Bank Balance",tracking = True)
    ira = fields.Char(string="401K / IRA",tracking = True)
    savings_account = fields.Char(string="Savings Account",tracking = True)
    business_owner = fields.Boolean(string="Business Owner",tracking = True)
    job_title = fields.Char(string="Job Title/Position",tracking = True)
    military = fields.Char(string="Military (Rank and Branch)",tracking = True)
    employer_state = fields.Many2one("res.country.state", string="Employer State",tracking = True)
    employer_zip = fields.Integer(string="Employer Zip",tracking = True)
    # previous_employer = fields.Char(string="Previous Employer",tracking = True)
    # previous_employment_month_year_hired = fields.Char(string="Previous Employment Month/Year Hired",tracking = True)




    """
        MORTGAGE AND RENT Fields On Affiliate Leads Form 
            Author : Wasif
    """

    rent_own = fields.Selection(
        [
            ('rent', 'Rent'),
            ('own', 'Own')
        ],
        string="Rent/Own",
        tracking = True
        )
    rent_payment = fields.Char(string="Rent Payment",tracking = True)
    mortgage_payment = fields.Char(string="Mortgage Payment",tracking = True)
    mortgage_company = fields.Char(string="Mortgage Company",tracking = True)
    mortgage_amount_owed = fields.Char(string="Mortgage Amount Owed",tracking = True)



    """
        BUSINESS INFO Fields On Affiliate Leads Form 
            Author : Wasif
    """


    business_name = fields.Char(string="Business Name",tracking = True)
    business_street = fields.Char(string="Business Street",tracking = True)
    business_state = fields.Many2one("res.country.state", string="Business State",tracking = True)
    business_city = fields.Char(string="Business City",tracking = True)
    business_phone = fields.Char(string="Business Phone",tracking = True)
    business_zip = fields.Integer(string="Business Zip",tracking = True)
    business_website = fields.Char(string="Business Website",tracking = True)
    use_of_proceeds = fields.Char(string="Use Of Proceeds",tracking = True)
    no_of_employees = fields.Integer(string="No. Of Employees",tracking = True)
    messaging_disclosure = fields.Boolean(string="Messaging Disclosure",tracking = True)
    ein_encrypted = fields.Char(string="EIN(Encrypted)",tracking = True)
    name_of_owner_and_percent_owned =fields.Char(string="Names of Owners and Percent Owned",tracking = True)
    years_in_business = fields.Integer(string="Years In Business",tracking = True)
    avg_daily_balance = fields.Char(string="Average Daily Balance",tracking = True)
    avg_monthly_revenue = fields.Integer(string="Average Monthly Revenue",tracking = True)
    no_of_bank_accounts = fields.Integer(string="Number of Bank Accounts",tracking = True)
    no_of_owners = fields.Integer(string="Number of Owners",tracking = True)
    annual_revenue = fields.Integer(string="Annual Revenue",tracking = True)
    industry_id = fields.Many2one("industry", string="Industry",tracking = True)
    total_business_loans = fields.Integer(string="Total Business Loans",tracking = True)
    percent_owner_1 = fields.Char(string="Percent Owner 1",tracking = True)
    percent_owner_2 = fields.Char(string="Percent Owner 2",tracking = True)
    # driver_licence_1  = fields.Char(string="Driver Licence No. 2",tracking = True)



    """
        CREDIT CARD AND PAYMENT DETAILS Fields On Affiliate Leads Form 
            Author : Wasif
    """

    credit_card_and_payment_details = fields.Text(string="Credit Card and Payment Details",tracking = True)
    
    
    
    
    """
        AFFILIATE INFO Fields On Affiliate Leads Form 
            Author : Wasif
    """

    affiliate_email = fields.Char(string="Affiliate Email",tracking = True)



    """
        Marketing/IP Address/Opt In/Misc Fields On Affiliate Leads Form 
            Author : Wasif
    """


    utm_keyword = fields.Char(string="UTM Keyword",tracking = True)
    utm_campaign = fields.Char(string="UTM Campaign",tracking = True)
    marketing_company = fields.Selection(
        [
            ('win_pearls', "Win Pearls")
        ],
        string="Marketing Company",
        tracking = True
    )
    disposition = fields.Char(string="Disposition",tracking = True)
    email_opt_out = fields.Boolean(string="Email Opt Out",tracking = True)
    mailing_source = fields.Char(string="Mailing Source",tracking = True)
    remail = fields.Char(string="Remail",tracking = True)
    promo_code = fields.Char(string="Promo Code",tracking = True)
    utm_source = fields.Char(string="UTM Source",tracking = True)
    utm_content = fields.Char(string="UTM Content",tracking = True)
    utm_medium = fields.Char(string="UTM Medium",tracking = True)
    retention_access = fields.Selection(
        [
            ('ncnr_sms_rvm', 'NCNR SMS/RVM'),
            ('declined_offer_sms_rvm', 'Declined Offer SMS/RVM')
        ],
        string="Retention Actions",
        tracking = True
    )
    in_home_date = fields.Date(string="In Home Date",tracking = True)
    mail_date = fields.Date(string="Mail Date",tracking = True)
    creative = fields.Char(string="Creative",tracking = True)
    bbb_review = fields.Boolean(string="BBB Review",tracking = True)
    dead_sent = fields.Boolean(string="Dead 60 Sent",tracking = True)
    res_ncnr_wf = fields.Boolean(string="Res NCNR/DO WF",tracking = True)



    """
        SYSTEM INFORMATION Fields On Affiliate Leads Form 
            Author : Wasif
    """


    created_by = fields.Char(string="Created By",tracking = True)
    # last_modified_by = fields.Char("ir.models.fields.write_uid", string="Last Modified By")
    last_seen_by = fields.Char(string="Last Seen By",tracking = True)
    next_activity_by = fields.Char(string="Next Activity By",tracking = True)
    last_activity_by = fields.Char(string="Last Activity By",tracking = True)
    owner_last_modified_by = fields.Char(string="Owner Last Modified By",tracking = True)
    timestamp_dead_decline_reason = fields.Char(string="Timestamp: Dead - Declined Reason",tracking = True)
    mgr_reviewed = fields.Boolean(string="MGR Reviewed",tracking = True)
    unused_field = fields.Char(string="UNUSED FIELD",tracking = True)
    date_created = fields.Date(string="Date Created",tracking = True)
    date_last_modified = fields.Date(string="Date Last Modified",tracking = True)
    date_last_seen = fields.Date(string="Date Last Seen",tracking = True)
    date_next_activity = fields.Date(string="Date Next Activity",tracking = True)
    date_last_activity = fields.Date(string="Date Last Activity",tracking = True)
    owner_last_modified = fields.Date(string="Owner Last Modified",tracking = True)
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
        tracking = True
    )
    csa_signed = fields.Boolean(string="CSA Signed",tracking = True)
    tijuana_assigned_timestamp = fields.Char(string="Tijuana Assigned Timestamp",tracking = True)



    """
        JA PERSONAL INFO Fields On Affiliate Leads Form 
            Author : Wasif
    """



    ja_first_name = fields.Char(string="JA First Name",tracking = True)
    ja_middle_name = fields.Char(string="JA Middle Name",tracking = True)
    ja_last_name = fields.Char(string="JA Last Name",tracking = True)
    ja_us_citizen = fields.Selection(
         [
            ('yes','Yes'),
            ('no','No')
        ],
        string="JA U.S Citizen",
        tracking = True
    )
    ja_date_of_birth = fields.Date(string="JA Date Of Birth",tracking = True)
    ja_social_security_number = fields.Char(string="JA Social Security Number",tracking = True)
    ja_home_address = fields.Char(string="JA Home Address",tracking = True)
    ja_moved_to_address = fields.Date(string="JA Moved To Address",tracking = True)
    ja_gross_annual_income = fields.Char(string="JA Gross Annual Income",tracking = True)
    ja_marital_status = fields.Selection(
            [
                ('single','Single'),
                ('married','Married'),
                ('divorced','Divorced')
            ],
            string="JA Marital Status",
            tracking = True
    )    
    ja_email = fields.Char(string="JA Email",tracking = True)
    ja_employer_name = fields.Char(string="JA Employer Name",tracking = True)
    ja_job_title = fields.Char(string="JA Job Title/Position",tracking = True)
    ja_employer_street = fields.Char(string="JA Employer Street",tracking = True)
    ja_employer_city = fields.Char(string="JA Employer City",tracking = True)
    ja_employer_state = fields.Many2one("res.country.state", string="JA Employer State",tracking = True)
    ja_employer_zip = fields.Integer(string="JA Employer Zip",tracking = True)
    ja_work_phone = fields.Char(string="JA Work Phone",tracking = True)
    ja_month_hired = fields.Char(string="JA Month/Year Hired",tracking = True)
    ja_rent_own = fields.Selection(
        [
            ('rent', 'Rent'),
            ('own', 'Own')
        ],
        string="Ja Own or Rent Home",
        tracking = True
        )
    ja_mortgage_company = fields.Char(string="JA Mortgage Company",tracking = True)
    ja_mortgage_payment = fields.Char(string="JA Mortgage Payment",tracking = True)
    ja_landlord = fields.Char(string="JA Landlord",tracking = True)
    ja_rent_payment = fields.Char(string="JA Rent Payment",tracking = True)
    


    """
        ARRAY INFO Fields On Affiliate Leads Form 
            Author : Wasif
    """


    array_grade = fields.Char(string="Array Grade",tracking = True)
    array_credit_score = fields.Char(string="Array Credit Score",tracking = True)
    array_debt_load = fields.Char(string="Array Debt Load",tracking = True)


    """
        CLOSEST RELATIVE Fields On Affiliate Leads Form 
            Author : Wasif
    """

    closest_relative = fields.Char(string="Closest Relative",tracking = True)
    relative_phone_number = fields.Integer(string="Relative Phone Number",tracking = True)
    affiliate_email = fields.Char(string="Affiliate Email",tracking = True)
    closest_relative_address = fields.Char(string="Closest Relative Address",tracking = True)
    


    """
        VERIFICATION INFO Fields On Affiliate Leads Form 
            Author : Wasif
    """

    verification_line_ids = fields.One2many(
        'lead.verification.line', 'lead_id',
        string="Verification Lines"
    )

    # credit_check_date = fields.Date(string="Credit Check Date",tracking = True)
    # new_credit_score = fields.Integer(string="New Credit Score",tracking = True)
    # need_cr_check = fields.Boolean(string="Need CR Check",tracking = True)
    # verified = fields.Boolean(string="Verified",tracking = True)
    # discrepancy = fields.Boolean(string="Discrepancy",tracking = True)
    # discrepancy_loan_amt = fields.Integer(string="Discrepancy Loan Amt",tracking = True)
    # discrepancy_reason = fields.Selection(
    #     [
    #         ('none','None'),
    #         ('collection_to_loan_amount','Collection To Loan Amount'),
    #         ('took_loan','Took Loan'),
    #         ('took_2nd_loan','Took 2nd Loan'),
    #         ('increased_original_amount','Increased Original Amount')
    #     ],string="Discrepancy Reason",
    #     tracking = True
    # )
    # discrepancy_status = fields.Selection(
    #     [
    #         ('none','None'),
    #         ('open','Open'),
    #         ('closed_not_playing','Closed Not Playing'),
    #         ('closed_no_response','Closed No Response'),
    #         ('closed_won','Closed Won'),
    #         ('sent_dispute_email','Sent Dispute Email'),
    #         ('sent_to_legal','Sent To Legal'),
    #         ('closed_verified','Closed Verified'),
    #         ('closed_won_payments','Closed Won Payments')
    #     ],string="Discrepancy Status",
    #     tracking = True
    # )
    # discrepancy_loan_date = fields.Date(string="Discrepancy Loan Date",tracking = True)
    # discrepancy_lender = fields.Char(string="Discrepancy Lender",tracking = True)
    # potential_fee_due = fields.Integer(string="Potential Fee Due",tracking = True)
    # mgr_reviewed = fields.Boolean(string="MGR Reviewed",tracking = True)
    # new_fee_collected_date = fields.Date(string="New Fee Collected Date",tracking = True)
    # processor_audit = fields.Selection(
    #     [
    #         ('no_final_email','No Final Email'),
    #         ('no_loan_savings','No Loan Savings'),
    #         ('no_biz_loan_options','No Biz Loan Options'),
    #         ('no_personal_loan_options','No Personal Loan Options'),
    #         ('missing_lender','Missing Lender'),
    #         ('closed_incorrectly_notes','Closed Incorrectly(Notes)'),
    #         ('send_to_drp','Send to DRP'),
    #         ('send_to_ertc','Send to ERTC'),
    #         ('send_to_ca_mortgage','Send to CA Mortgage'),
    #         ('incorrect_dead_sales_reason','Incorrect Dead Sales Reason'),
    #         ('missing_emails','Missing Email(s)'),
    #         ('see_mgr','See MGR'),
    #         ('missing_generated_email','Missing Generated email'),
    #         ('password_incorrect_format','Password incorrect format'),
    #         ('missing_income_household','Missing Income/ Household'),
    #         ('missing_loan_amount','Missing/Wrong Loan amount'),
    #         ('missing_ja_income','Missing JA Income'),
    #         ('wrong_stage','Wrong Stage'),
    #         ('missing_info','Missing Info'),
    #         ('incorrect_lender','Incorrect Lender')
    #     ],
    #     string="Processor Audit",
    #     tracking = True
    # )
    # apps_error = fields.Selection(
    #     [
    #         ('missing_ss','Missing/wrong screenshot'),
    #         ('no_max_amount','No Max amount'),
    #         ('not_using_personal_email','Not using personal e-mail'),
    #         ('didnt_select_offer','Didnt select offer on LQ/Upstart'),
    #         ('didnt_verify_cr','Didnt verify CR for existing loans'),
    #         ('closed_incorrectly','Closed Incorrectly'),
    #         ('application_typo','Application Typo'),
    #         ('applied_wrong_amount','Applied wrong amount'),
    #         ('Wrong_status','Wrong status'),
    #         ('wrong_lender_info','Wrong lender Info'),
    #         ('did_not_follow_apps_rules','Did not follow apps rules'),
    #         ('incomplete_cr_detail','Incomplete CR Detail'),
    #         ('wrong_cr_detail','Wrong CR detail'),
    #         ('wrong_client_info_used','Wrong client info used')
    #     ],
    #     string="Apps Error",
    #     tracking = True
    # )
    # new_amt_collected = fields.Integer(string="New Amt Collected",tracking = True)
    # added_lender_error = fields.Selection(
    #     [
    #         ('missing_ss_no_max_amount','Missing/wrong screenshot No Max amount'),
    #         ('not_using_personal_email','Not using personal e-mail'),
    #         ('didnt_select_offer','Didnt select offer on LQ/Upstart'),
    #         ('didnt_veriy_cr','Didnt verify CR for existing loans'),
    #         ('closed_incorrectly','Closed Incorrectly'),
    #         ('application_typo','Application Typo'),
    #         ('applied_wrong_amount','Applied wrong amount')
    #     ],
    #     string="Added Lender Error",
    #     tracking = True
    # )
    # sales_error = fields.Selection(
    #     [
    #         ('blank','Blank'),
    #         ('missing_wrong_income','Missing/wrong Income'),
    #         ('typo','Typo'),
    #         ('missing_mtg_rent','Missing MTG/ Rent'),
    #         ('missing_college_info','Missing College info'),
    #         ('wrong_info','Wrong Info'),
    #         ('missing_wrong_employer_info','Missing/wrong Employer info'),
    #         ('no_ssn','No SSN'),
    #         ('missing_wrong_employer_info','Missing/wrong Retired info'),
    #         ('converted_incorrectly','Converted Incorrectly'),
    #         ('csa_not_signed','CSA not signed'),
    #         ('missing_cr_wrong_cr','Missing CR/Wrong CR')
    #     ],
    #     string="Sales Error",
    #     tracking = True
    # )
    # to_call = fields.Boolean(string="To Call",tracking = True)
    # shark_tank = fields.Boolean(string="Shark Tank",tracking = True)
    # apps_audit = fields.Boolean(string="APPS AUDIT",tracking = True)





    """
        PROCESSING Form Fields 
            Author : Wasif
    """



    dead_sale_id = fields.Many2one('dead.sale',string="Dead Sale",tracking = True)
    sp_declined_all_call = fields.Boolean(string="SP Declined All Call",tracking = True)
    expected_revenue = fields.Integer(string="Expected Revenue",tracking = True)
    amount = fields.Monetary(string="Amount",compute="_compute_amount",store=True, currency_field='currency_id',tracking = True)
    loan_amount = fields.Monetary(string="Loan Amount", currency_field='currency_id',tracking = True)
    add_app_loan_result = fields.Selection(
        [
            ('declined_all','Declined All'),
            ('poor','Poor (1-2 approvals over 20%)'),
            ('fair','Fair (1-2 approvals over 15%-19.9%)'),
            ('good','Good (1-2 approvals under 15%)')
        ],
        string="Add App Loan Result",
        tracking = True
    )
    app_result = fields.Selection(
        [
            ('declined_all','Declined All'),
            ('declined_all_one_main_approval','Declined All-OneMain Approval'),
            ('poor','Poor (1-2 approvals over 20%)'),
            ('fair','Fair (1-2 approvals over 15%-19.9%)'),
            ('good','Good (1-2 approvals under 15%)')
        ],
        string="App Result",
        tracking = True
    )
    close_date = fields.Date(string="Close Date",tracking = True)
    lender_list = fields.Text(string="Lender List",tracking = True)


    @api.depends('client_fee','loan_amount')
    def _compute_amount(self):
        for record in self:
            if record.client_fee and record.loan_amount:
                record.amount = (
                    record.loan_amount * (record.client_fee / 100)
                ) 
            else:
                record.amount = 0
    
    @api.depends('total_current_balance','total_high_credit')
    def _compute_utilization_rate(self):
        for record in self:
            if record.total_current_balance and record.total_high_credit:
                record.revolving_credit_utilization = (
                    record.total_current_balance / record.total_high_credit
                ) 
            else:
                record.revolving_credit_utilization = 0

    """
    Truth And Closure Fields  Form Fields
        Author : Wasif
    """
    
    deposit_amount = fields.Integer(string="Deposit Amount",tracking = True)
    amount_client_w = fields.Integer(string="Amount Client Walks Away With",tracking = True)
    date_funds_scheduled = fields.Date(string="Date Funds are Scheduled For Draft",tracking = True)
    loan_amount = fields.Integer(string="Loan Amount",tracking = True)
    lender_origination_fee = fields.Integer(string="Lender Origination Fee",tracking = True)

    
    """
    Creditor Form Fields
        Author : Wasif
    """
    line_id = fields.One2many('creditors','creditor_crm_id',string="Creditor Line ID")

    debt_monthly_payment = fields.Monetary(string="Monthly Payment", currency_field='currency_id',tracking=True)
    total_current_balance = fields.Monetary(string="Total Current Balance", currency_field='currency_id',tracking=True)
    total_high_credit = fields.Monetary(string="Total High Credit", currency_field='currency_id',tracking=True)
    loan_amount = fields.Monetary(string="Loan Amount", currency_field='currency_id',tracking=True)
    loan_monthly_payment = fields.Monetary(string="Monthly Payment", currency_field='currency_id',tracking=True)
    loan_term = fields.Integer(string="Term",tracking=True)
    lender_name = fields.Char(string="Lender Name",tracking=True)
    # Bilal add Attachment Field
    attachment_ids = fields.One2many('crm.attachment', 'crm_id', string='Attachments')


    # @api.depends("line_id.current_balance")
    def computetcb(self): 
        total_current_balance=0
        debt_monthly_payment=0
        total_high_credit = 0
        for line in self.line_id:
            if line.select_creditor == True:
                # raise UserError("hehe")
                total_current_balance += line.current_balance
                debt_monthly_payment += line.monthly_payment
                total_high_credit += line.high_credit
        self.total_current_balance = total_current_balance
        self.debt_monthly_payment = debt_monthly_payment
        self.total_high_credit = total_high_credit


    """
    Lender Form Fields
        Author : Wasif
    """

    # The code `lender_line` is a comment in Python. Comments are used to provide explanations or
    # annotations in the code for better understanding by humans. In this case, the comment seems to
    # be a placeholder or a section divider denoted by the `
    lender_line_id = fields.One2many('lender.line','crm_id',string="Lender Line ID")
    # lender_id = fields.Many2one('lenders',string="Lender")
    # lender_update = fields.Char(string="Lender Update",related="lender_id.lender_update")
    # lender_benefit = fields.Char(string="Lender Benefit",related="lender_id.lender_benefit")
    # lender_description = fields.Text(string="Lender Description",related="lender_id.lender_description")
    # how_to_secure  = fields.Char(string="How To Secure",related="lender_id.how_to_secure")
    # how_to_present_lender  = fields.Char(string="How To Present Lender",related="lender_id.how_to_present_lender")
    # static_note = fields.Char(string="Static Note",related="lender_id.static_note")
    # lender_phone  = fields.Integer(string="Phone",related="lender_id.phone")
    # status = fields.Selection(
    #     [
    #         ('active','Active'),
    #         ('inactive','Inactive')
    #     ],string="Status"
    #     ,related="lender_id.status"
    # )
    # web_address = fields.Char(string="Web Address",related="lender_id.web_address")
    # lender_support_email = fields.Char(string="Lender Support Email",related="lender_id.lender_support_email")





    """
    NOTES Form Fields
        Author : Wasif
    """

    notes = fields.Text(string="NOTES")
    processor_notes = fields.Text(string="Processor Notes")


    """
    FLAGS Form Fields
        Author : Wasif
    """
    
    
    flag_code_line = fields.One2many('flags.line.id','crm_id', string="Code")

   
    """
    SCRIPTS Form Fields
        Author : Wasif
    """
    script_id = fields.Many2one('script',string="Script")
    description = fields.Text(string="Description", compute="computeScript")

    is_pull_equifex = fields.Boolean("Is Pull Equifex")
    is_pull_crs = fields.Boolean("Is Pull Equifex")
    
    
    
    """
    INTRODUCTORY TAB Form Fields
        Author : Wasif
    """

    introduction_ssn = fields.Integer(string="SSN",tracking=True)
    introduction_email = fields.Char(string="Email",tracking=True)
    introduction_phone = fields.Char(string="Phone",tracking=True)
    introduction_loan_amount = fields.Char(string="Loan Amount",tracking=True)
    introduction_search = fields.Char(string="What Are You Looking To Accomplish?",tracking=True)
    introduction_interest_rate = fields.Char(string="CC/Interest Rates",tracking=True)
    introduction_amount_debt = fields.Char(string="Amount Of Debt?",tracking=True)
    introduction_to_be_funded = fields.Char(string="How quickly would you like to be funded?",tracking=True)
    introduction_vgi = fields.Char(string="What is your VGI",tracking=True)
    introduction_tax_return = fields.Char(string="Verifiable by Pay stub or Tax Return? Which one?",tracking=True)
    introduction_pay_frequency = fields.Char(string="Pay Frequency",tracking=True)
    introduction_co_app = fields.Char(string="Co-App Yes Or No",tracking=True)
    introduction_self_employed = fields.Char(string="Self Employed/Biz Yes or No?",tracking=True)
    introduction_docs = fields.Char(string="Doc Yes or No?",tracking=True)


    @api.depends("script_id")
    def computeScript(self):
        for rec in self:
            rec["description"] = False            
            if rec.script_id:
                rec["description"] = rec.script_id.description

    
   
    def login_equifex(self):
        url = f'{PROTOCOL}://{EQ_SENDBOX_HOST}/{EQ_VESION}/oauth/token'



        payload = EQ_PAYLOAD
        headers = EQ_HEADERS
        auth = HTTPBasicAuth(EQ_USERNAME, EQ_PASSWORD)
        response = requests.request("POST", url, auth=auth, headers=headers, data=payload)

        if response.status_code == 200:
        # Assuming response is JSON and contains 'token' field
            data = response.json()
            if 'access_token' in data:
                return data['access_token']
            else:
                raise UserError("Login successful but token not found in the response")
        else:
            raise UserError(f"Failed to login. Status: {response.status_code}, Response: {response.text}")



    def action_pull_equifax(self):
        """"""
        token = self.login_equifex()
        try:

            url = f"{PROTOCOL}://{EQ_SENDBOX_HOST}/business/oneview/consumer-credit/v1/reports/credit-report"

            payload = json.dumps({
            "consumers": {
                "name": [
                {
                    "identifier": "Current",
                    "firstName": "PLAZDWA",
                    "middleName": "k",
                    "lastName": "AEJRZ",
                    "suffix": ""
                }
                ],
                "socialNum": [
                {
                    "identifier": "Current",
                    "number": "666001590"
                }
                ],
                "dateOfBirth": "03021954",
                "age": "",
                "addresses": [
                {
                    "identifier": "Current",
                    "streetName": "482 ALSNHW TA",
                    "city": "FPOSANFRANCISCO",
                    "state": "CA",
                    "zip": "96603"
                }
                ],
                "phoneNumbers": [
                {
                    "identifier": "Current",
                    "number": ""
                }
                ]
            },
            "customerReferenceIdentifier": "2C800002-DOR7",
            "customerConfiguration": {
                "equifaxUSConsumerCreditReport": {
                "pdfComboIndicator": "Y",
                "memberNumber": "999FZ18093",
                "securityCode": "@U1",
                "codeDescriptionRequired": True,
                "protocolIndicator": 2,
                "customerCode": "IAPI",
                "ECOAInquiryType": "Individual",
                "optionalFeatureCode": [
                    ""
                ],
                "endUserInformation": {
                    "endUsersName": "abcd",
                    "permissiblePurposeCode": "01"
                }
                }
            }
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            if not self.is_pull_equifex and self.is_pull_crs:
                raise UserError("You are not able to pull equifax because CRS is already Pulled")
            response = requests.request("POST", url, headers=headers, data=payload) 
            data = response.json()
            # date_opened = datetime.strptime(data['consumers']['equifaxUSConsumerCreditReport']['fileSinceDate'], "%d%m%Y").date()
            # effective_date = datetime.strptime(data['consumers']['equifaxUSConsumerCreditReport']['reportDate'], "%d%m%Y").date()
            credits = []

            consumers = data.get('consumers', {})

            if not isinstance(consumers, dict):
                raise UserError(f"Expected 'consumers' to be a dictionary, got {type(consumers)}")

            credit_report = consumers.get('equifaxUSConsumerCreditReport', [])
            if not isinstance(credit_report, list):
                raise UserError(f"Expected 'equifaxUSConsumerCreditReport' to be a dictionary, got {type(credit_report)}")

            trades = credit_report[0].get('trades', [])
            if not isinstance(trades, list):
                raise UserError(f"Expected 'trades' to be a list, got {type(trades)}")

            if not trades:
                raise UserError("Trades not found in the data.")

            # raise UserError(str(trades))
            
            # raise UserError(str(trades))
            for crds in trades:

                # raise UserError(crds['portfolioTypeCode']['description'])
                # raise UserError(str(crds['termsFrequencyCode']))
                if "Mortgage" not in crds['portfolioTypeCode'].get('description',''):
                    credits.append((0,0,{
                        'date_opened':datetime.strptime(crds['dateReported'], "%m%d%Y").date().isoformat(),
                        'effective_date':datetime.strptime(crds['dateOpened'], "%m%d%Y").date().isoformat(),
                        'name':crds['customerNumber'],
                        'high_credit':crds['highCredit'],
                        'current_balance': crds.get('balance', 0),
                        'monthly_payment' : crds.get('pastDueAmount', 0),
                        'portfolio_type': crds.get('portfolioTypeCode',''),
                        'term': crds['termsFrequencyCode'].get('description',''),
                    }))
            # raise UserError(str(credits))
            self.write({
                'line_id':credits,
                'is_pull_equifex':True
                # 'flag_code_line':flags
            })

                        # Constants for retry mechanism
            MAX_RETRIES = 2  # Maximum number of retries
            RETRY_DELAY = 30  # Delay between retries in seconds

            # Step 7: Fetch the PDF Report
            pdf_url = f"{PROTOCOL}://{EQ_SENDBOX_HOST}{data.get('links', [])[0]['href']}"

            pdf_headers = {
                'Authorization': f'Bearer {token}'
            }

            if not pdf_url:
                raise UserError("PDF URL not found in the response.")

            # Retry logic for fetching the PDF
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    pdf_response = requests.get(pdf_url, headers=pdf_headers)
                    
                    # Check if the PDF is ready
                    if pdf_response.status_code == 200:
                        # PDF fetched successfully
                        pdf_content = pdf_response.content
                        file_name = f"Equifax_Report_{self.id}.pdf"

                        # Save the PDF as an attachment
                        self.env['ir.attachment'].create({
                            'name': file_name,
                            'type': 'binary',
                            'datas': base64.b64encode(pdf_content),
                            'res_model': self._name,
                            'res_id': self.id,
                            'mimetype': 'application/pdf',
                        })

                        self.message_post(
                            body=f"Equifax report fetched successfully and attached as '{file_name}'.",
                            subtype_id=self.env.ref('mail.mt_note').id
                        )
                    elif pdf_response.status_code == 409:
                        # PDF generation in progress
                        error_details = pdf_response.json().get('additionalErrorDetails', {})
                        error_message = error_details.get('message', 'PDF generation in progress')
                        time_stamp = error_details.get('timeStamp', 'unknown time')

                        # Log and wait before retrying
                        if attempt < MAX_RETRIES:
                            time.sleep(RETRY_DELAY)
                            continue
                        else:
                            raise UserError(f"Failed after {MAX_RETRIES} retries: {error_message} (Last attempt at {time_stamp})")
                    else:
                        # Other HTTP errors
                        raise UserError(f"Unexpected error: {pdf_response.status_code} - {pdf_response.text}")

                except requests.exceptions.RequestException as e:
                    raise UserError(f"An error occurred while fetching the PDF report: {str(e)}")
                    
        except Exception as e:
            # Log Error in Chatter
            raise UserError(str(e))
            self.message_post(
                body=f"An error occurred while fetching the Equifax report: {str(e)}",
                subtype_id=self.env.ref('mail.mt_note').id
            )
                # Optionally, you can re-raise the error if needed

    

    def login_transunion(self):
        
        url = f'{PROTOCOL}://{SANDBOX_HOST}:{PORT}{BASE_URL}/users/login'



        payload = json.dumps({
            "username": USERNAME,
            "password": PASSWORD
        })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
        # Assuming response is JSON and contains 'token' field
            data = response.json()
            if 'token' in data:
                return data['token']
            else:
                raise UserError("Login successful but token not found in the response")
        else:
            raise UserError(f"Failed to login. Status: {response.status_code}, Response: {response.text}")



    
    def pull_credit_transunion_json(self):
            """
            Fetches data from the TransUnion API, handles responses, and adds logs and attachments to the Chatter.
            Author: "Bilal Memon"
            """
            try:
                # Step 1: Login to get the token
                token = self.login_transunion()  # Ensure this method is defined separately
                if not token:
                    raise UserError("Failed to retrieve authentication token.")

                # Step 2: Define API URLs
                base_url = f'{PROTOCOL}://{SANDBOX_HOST}:{PORT}{BASE_URL}'
                json_url = f'{base_url}/transunion/credit-report/basic/tu-prequal-vantage4'
                pdf_url_template = f'{base_url}/transunion/custom-credit-report/pdf/{{request_id}}/tu-prequal-vantage4'

                # Step 3: JSON Payload
                payload = json.dumps({
                    "firstName": "ZELNINO",
                    "middleName": "X",
                    "lastName": "WINTER",
                    "nameSuffix": "SR",
                    "street1": "760 W SPROUL RD",
                    "city": "FANTASY ISLAND",
                    "state": "IL",
                    "zip": "60750",
                    "ssn": "666125812",
                    "dob": "1977-06-01",
                    "phone": "0000000000"
                })

                # Step 4: API Headers
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': f'Bearer {token}'
                }
                if self.is_pull_equifex and not self.is_pull_crs:
                    raise UserError("You are not able to pull CRS because Equifax is already Pulled")
                
                # Step 5: Make the JSON Request
                response = requests.request("POST", json_url, headers=headers, data=payload)
                res = response.json()
                creditor = []
                flags = []

                # raise UserError(str(res))
                for crds in res['custom']['credit']['trades']:
                    creditor.append((0, 0, {
                        'name': crds['subscriber']['name']['unparsed'] if crds.get('subscriber') and crds['subscriber'].get('name') else '',
                        'portfolio_type': crds.get('portfolioType', ''),
                        'account_number': crds.get('accountNumber', ''),
                        'date_opened': crds['dateOpened']['value'] if crds.get('dateOpened') and crds['dateOpened'].get('value') else '',
                        'current_balance': crds.get('currentBalance', 0),
                        'term': crds['terms']['paymentScheduleMonthCount'] if crds.get('terms') and crds['terms'].get('paymentScheduleMonthCount') else '',
                        'monthly_payment': crds.get('amount', 0),
                        'high_credit': crds.get('highCredit', ''),
                        'status': crds.get('ecoadesignator', ''),
                        'effective_date': crds['dateEffective']['value'] if crds.get('dateEffective') and crds['dateEffective'].get('value') else '',
                        'creditor_crm_id':self.id    
                    }))
                    
                
                for flag in res['addOnProducts']:
                    if 'scoreModel' in flag and 'score' in flag['scoreModel'] and 'factors' in flag['scoreModel']['score']:
                        for factor in flag['scoreModel']['score']['factors'].get('factors', []):
                            flags.append((0, 0, {
                                'flag_code': self.env['flags.lead'].search([('name','=',factor.get('code', ''))]).id  # Use .get to safely retrieve the value
                            }))
                self.write({
                    'line_id':creditor,
                    'is_pull_crs':True,
                    'flag_code_line':flags
                })
                # raise UserError(str(flags) + '====='+ str(creditor))
                data = {}
                if response.status_code != 200:
                    raise UserError(f"Failed to fetch JSON data. Error: {response.text}")

                # Step 6: Extract Request ID from Headers
                request_id = response.headers.get('RequestID')
                if not request_id:
                    raise UserError("Request ID not found in response headers.")

                # Step 7: Fetch the PDF Report
                pdf_url = pdf_url_template.format(request_id=request_id)
                pdf_headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/pdf',
                    'Authorization': f'Bearer {token}'
                }

                pdf_response = requests.request("POST", pdf_url, headers=pdf_headers)
                if pdf_response.status_code != 200:
                    raise UserError(f"Failed to fetch PDF report. Error: {pdf_response.text}")

                # Step 8: Save the PDF as an Attachment
                pdf_content = pdf_response.content
                file_name = f"TransUnion_Report_{request_id}.pdf"

                self.env['ir.attachment'].create({
                    'name': file_name,
                    'type': 'binary',
                    'datas': base64.b64encode(pdf_content),
                    'res_model': self._name,
                    'res_id': self.id,
                    'mimetype': 'application/pdf',
                })

                # Step 9: Log Success
                self.message_post(
                    body=f"TransUnion report fetched successfully and attached as '{file_name}'.",
                    subtype_id=self.env.ref('mail.mt_note').id
                )

            except Exception as e:
                # Log Error in Chatter
                self.message_post(
                    body=f"An error occurred while fetching the TransUnion report: {str(e)}",
                    subtype_id=self.env.ref('mail.mt_note').id
                )
                # Optionally, you can re-raise the error if needed
                raise UserError(f"An error occurred: {str(e)}")
    

    # def action_open_csa_general_wizard(self):
    #     return {
    #         'name': 'CSA General Agreement',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'csageneral.agreement',
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'context': {
    #             'default_crm_lead_id': self.id,
    #             'default_email': self.email,
    #             'default_phone': self.phone,
    #             'default_street': self.street,
    #             'default_yearly_income': self.primary_gross_annual_income,
    #             'default_is_income_verifiable': '',
    #             'default_no_10': '',  # Placeholder if you have additional logic for these
    #             'default_no_11': '',
    #             'default_change_fee': '',
    #         }
    #     }





# class CreditorLine(models.Model):
#     _name="creditor.line"

#     # company_id = fields.Many2one('res.company',default=lambda self: self.env.company.id,)
#     creditor_crm_id = fields.Many2one('crm.lead',string="Creditors")  
#     creditor_id = fields.Many2one('creditors',string="Creditor") 
#     select_creditor = fields.Boolean(string="Select")
#     portfolio_type = fields.Char(string="Portfolio Type",related="creditor_id.portfolio_type")
#     type = fields.Char(string="Type",related="creditor_id.type")
#     account_number = fields.Char(string="Account Number",related="creditor_id.account_number")
#     date_reported = fields.Date(string="Date Reported",related="creditor_id.date_reported")
#     date_opened = fields.Date(string="Date Opened",related="creditor_id.date_opened")
#     credit_limit = fields.Float(string="Credit Limit",related="creditor_id.credit_limit")
#     current_balance = fields.Float(string="Balance",related="creditor_id.current_balance")
#     term = fields.Char(string="Term",related="creditor_id.term")
#     monthly_payment = fields.Float(string="Monthly Payment",related="creditor_id.monthly_payment")
#     status = fields.Char(string="Status",related="creditor_id.status")
#     customer_number = fields.Char(string="Customer Number",related="creditor_id.customer_number")

#     name = fields.Char(string="Creditor")
#     # balance = fields.Integer(string="Balance")
#     # monthly_payment = fields.Integer(string="Monthly Payment")
#     # type = fields.Char(string="Type")




class LenderLine(models.Model):
    _name="lender.line"
    _inherit = 'mail.thread'


    # company_id = fields.Many2one('res.company',default=lambda self: self.env.company.id,)
    crm_id = fields.Many2one('crm.lead',string="Crm")
    lender_id = fields.Many2one('lenders',string="Lender",tracking=True)
    name = fields.Char(string="Lender Name",tracking=True)
    creditor_status_ = fields.Many2one('creditors.status',string="Status")
    select = fields.Boolean(string="Select",tracking=True)
    status = fields.Selection(
        [
            ('active','Active'),
            ('inactive','Inactive')
        ],string="Status"
        ,related="lender_id.status",tracking=True
    )
    pre_approved_amount = fields.Integer(string="Pre-Approved Amount",tracking=True)
    approved_amount = fields.Integer(string="Approved Amount",tracking=True)
    max_amount = fields.Integer(string="Max Amount",tracking=True)
    loan_term = fields.Char(string="Loan Term",tracking=True)
    interest_buy_rate = fields.Char(string="Interest/Buy Rate",tracking=True)
    payment = fields.Char(string="Payment",tracking=True)
    collection_amount = fields.Integer(string="Collection Amount",tracking=True)
    original_fee = fields.Integer(string="Original Fee",tracking=True)
    commission = fields.Char(string="Commission %",tracking=True)
    fee_reduced_reason = fields.Selection(
        [
            ('lender_fee','Lender Fee'),
            ('save_sale','Save Sale'),
            ('dead','Dead 60'),
            ('to','TO'),
            ('multiple_loan','Multiple Loan'),
            ('wt_discount','WT Discount')
        ],
        string="Fee Reduced Reason",
        tracking = True
    )
    added_lender = fields.Boolean(string="Added Lender")
    notes = fields.Char(string="Notes")
    chargeback_reason = fields.Selection(
        [
            ('nsf','NSF'),
            ('wrong','Wrong Account Info'),
            ('cancelled','Customer Cancelled Loan'),
            ('declined','Bank Declined'),
            ('waiting','Waiting To Fund')
        ],
        string="Chargeback Reason",
        tracking = True
    )
    funds_avail_date = fields.Date(string="Funds Avail Date")
    app_run_date = fields.Date(string="App Run Date")
    docs_loans = fields.Selection(
        [
            ('docs','Docs'),
            ('no_docs','No Docs')
        ],
        string="Docs/No Docs Loans",
        tracking = True
    )
    renewal_date = fields.Date(string="Renewal Date")
    maturity_date = fields.Date(string="Maturity Date")
    loan_outcome = fields.Selection(
        [
            ('active','Active'),
            ('active_renewal','Active, Renewal'),
            ('active_declined_drop','Active, Declined Renewal, Drop In Revenue'),
            ('active_declined','Active, Declined Renewal, Try in 30'),
            ('active_eligible','Active, Eligible for Renew, Unresponsive'),
            ('active_denied','Active, Denied Offer to Renew'),
            ('active_sub_docs','Active, Sub Docs for Renew'),
            ('suspended','Suspended'),
            ('denied','Denied, Renewal Offer Completed'),
            ('defaulted','Defaulted'),
            ('lowered_payments','Lowered Payments'),
            ('paid_refused','Paid in Full, Refused to Renew'),
            ('paid_renewed','Paid in Full, Renewed Again'),
            ('paused_payments','Paused Payments')
        ],
        string="Loan Outcome",
        tracking = True
    )
    fee_basis_amount = fields.Integer(string="Fee Basis Amount")
    days_final_approval = fields.Integer(string="Days To Final Approval")
    



    def write(self, vals):
        
        lenders_initial_values = defaultdict(dict)

        tracking_fields = []
        for field_name in vals:
            field = self._fields[field_name]
            if not (hasattr(field, 'related') and field.related) and hasattr(field, 'tracking') and field.tracking:
                tracking_fields.append(field_name)
        fields_definition = self.env['lender.line'].fields_get(tracking_fields)

        # Get initial values for each account
        for account in self:
            for field in tracking_fields:
                # Group initial values by partner_id
                lenders_initial_values[account][field] = account[field]

        res = super().write(vals)

        # Log changes to move lines on each move
        for lender, initial_values in lenders_initial_values.items():
            tracking_value_ids = lender._mail_track(fields_definition, initial_values)[1]
            if tracking_value_ids:
                msg = _("Lenders %s updated", lender._get_html_link(title=f"#{lender.lender_id.name}"))
                lender.crm_id._message_log(body=msg, tracking_value_ids=tracking_value_ids)
                if 'crm_id' in initial_values:  # notify previous partner as well
                    initial_values['crm_id']._message_log(body=msg, tracking_value_ids=tracking_value_ids)
        return res


    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for lender in res:
            msg = _("Lender %s created", lender._get_html_link(title=f"#{lender.lender_id.name}"))
            lender.crm_id._message_log(body=msg)
        return res


    def unlink(self):
        # EXTENDS base res.partner.bank
        for lender in self:
            msg = _("Lender %s deleted", lender._get_html_link(title=f"#{lender.lender_id.name}"))
            lender.crm_id._message_log(body=msg)
        return super().unlink()

    
class CRMAttachment(models.Model):
    _name = 'crm.attachment'
    _description = 'CRM Attachment'

    crm_id = fields.Many2one('crm.lead', string='CRM Lead', ondelete='cascade')
    attachment_ids = fields.Many2many('ir.attachment', 'crm_attachment_attachment_rel', 'crm_id',
                                      'attachment_id', 'Attachments',
                                      help="You may attach files to this template, to be added to all "
                                           "emails created from this template")
    uploaded_by = fields.Many2one('res.users', string='Uploaded By', default=lambda self: self.env.user, readonly=True)
    upload_date = fields.Datetime(string='Upload Date', default=fields.Datetime.now, readonly=True)

































