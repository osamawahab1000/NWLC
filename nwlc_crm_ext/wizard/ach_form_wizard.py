from odoo import _,api,fields,models
from odoo.exceptions import UserError

import base64
import threading

class ACHFormWizard(models.TransientModel):
    _name = "ach.form"
    _inherit = ['mail.thread',
                'mail.activity.mixin',
                'mail.render.mixin',
    ]
    # name = fields.Char('crm.lead','name',string="Name")
    crm_lead_id = fields.Many2one('crm.lead', string="CRM Lead")

    full_name = fields.Char(string="Customer Name")
    amount = fields.Char(string="Amount")
    email = fields.Char(string="Email")
    bank_name = fields.Char(string="Bank Name")
    bank_routing_number = fields.Char(string="Bank Routing Number")
    bank_account_number = fields.Char(string="Bank Account Number")
    date_funds_avail = fields.Datetime(string="Date Funds Available")
    account_type = fields.Selection(
        [
            ('checking','Checking'),
            ('savings','Savings')
        ],string="Account Type"
    )
    


    def print_ach_form(self):
        """Trigger the CRM Lead report printing."""
        self.ensure_one()  # Ensure only one wizard is active 
        self.crm_lead_id.account_type  = self.account_type 
        self.crm_lead_id.bank_name = self.bank_name 
        self.crm_lead_id.bank_routing_number = self.bank_routing_number 
        self.crm_lead_id.bank_account_number = self.bank_account_number 
        self.crm_lead_id.date_funds_avail = self.date_funds_avail 
        # data = {'data':self.crm_lead_id,'extra':self.no_10}
        return self.env.ref('nwlc_crm_ext.action_ach_form_template').report_action(self.crm_lead_id)
    

    # def send_ach_form(self):
    #     """Generate the QWeb report and send it as an email attachment from the wizard."""

    #     # Ensure an email is provided
    #     if not self.email:
    #         raise UserError(_("Please provide an email address to send the report."))

    #     report  = self.env['ir.actions.report']._render_qweb_pdf("nwlc_crm_ext.action_ach_form_template",self.crm_lead_id.id)
    #     if not report:
    #         raise UserError(_("The report template was not found."))


    #         # Create an email attachment
    #     attachment = self.env['ir.attachment'].create({
    #         'name': f"ACH Form.pdf",
    #         'type': 'binary',
    #         'datas': base64.b64encode(report[0]),  # Encode PDF to Base64
    #         'res_model': 'crm.lead',
    #         'res_id': self.crm_lead_id.id,
    #         'mimetype': 'application/pdf',
    #     })

    #     # Prepare email values
    #     template = self.env.ref('nwlc_crm_ext.email_template_ach_form')  # Replace with your template ID
    #     template.send_mail(
    #         self.crm_lead_id.id,  # CRM Lead ID as the recipient
    #         force_send=True,  # Send immediately
    #         email_values={
    #             'email_to': self.email,
    #             'attachment_ids': [(4, attachment.id)],  # Add the generated PDF as an attachment
    #         }
    #     )
    #     return {'type': 'ir.actions.act_window_close'}


    # def send_ach_form(self):
    #     if not self.email:
    #         raise UserError(_("Please provide an email address."))
     
    #     # Generate ACH PDF
    #     pdf_report = self.env['ir.actions.report']._render_qweb_pdf("nwlc_crm_ext.action_ach_form_template", self.crm_lead_id.id)
    #     if not pdf_report:
    #         raise UserError(_("Could not generate report."))

    #     pdf_data = pdf_report[0]

    #     # Create an attachment for sign request
    #     attachment = self.env['ir.attachment'].create({
    #         'name': "ACH Form.pdf",
    #         'type': 'binary',
    #         'datas': base64.b64encode(pdf_data),
    #         'res_model': 'sign.template',
    #         'res_id': 3,
    #         'mimetype': 'application/pdf',
    #     })

    #     # Load a Sign template (or create one programmatically if needed)
    #     sign_template = self.env.ref('nwlc_crm_ext.email_template_ach_form')  # You must create this template in Sign app
        
    #     template_id = self.env['sign.template'].search([('id','=',3)])
    #     template_id.write({
    #         'attachment_id': attachment.id,
    #     })
    
       
    #     # Create sign request
    #     sign_request = self.env['sign.request'].create({
    #         'template_id': template_id.id,
    #         'reference': f"ACH Signature for {self.crm_lead_id.name}",
    #         'request_item_ids': [(0, 0, {
    #             'partner_id': self.crm_lead_id.full_name.id,
    #             'role_id': 1,  # Assuming one role
    #             'mail_sent_order': 1,
    #         })],
    #     })

    #     # Send sign request via email

    #     return {
    #         'type': 'ir.actions.act_window_close'
    #     }


    def send_ach_form(self):
        if not self.crm_lead_id:
            raise UserError(_("No associated CRM lead found."))

        # 1. Generate ACH PDF
        pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(
            "nwlc_crm_ext.action_ach_form_template", 
            self.crm_lead_id.id
        )

        if not pdf_content:
            raise UserError(_("Could not generate ACH form."))

        # 2. Get or create template with proper roles
        template = self.env.ref('nwlc_crm_ext.ach_form_template', raise_if_not_found=False)
        attachment = self.env['ir.attachment'].create({
            'name': f"{self.crm_lead_id.name}_ACH_sign_Document.pdf",
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': 'sign.template',
        })
        if not template:
            # Create template with proper role if doesn't exist
            template = self.env['sign.template'].create({
                'name': 'ACH Form Template',
                'attachment_id': attachment.id,
                'sign_item_ids': [
                    (0, 0, {
                        'name': 'Customer Signature',
                        'type_id': self.env.ref('sign.sign_item_type_signature').id,
                        'required': True,
                        'page': 1,
                        'posX': 0.5,
                        'posY': 0.8,
                        'width': 0.3,
                        'height': 0.1,
                        'responsible_id':1,
                    }),
                ]
            })
        
        # 3. Update template with new PDF
        
        self.env['ir.attachment'].search([('id','=',attachment.id)]).write({
            'res_id': template.id,
        })

        # template.write({'attachment_id': attachment.id})

        # 4. Create sign request with proper role mapping
        sign_request = self.env['sign.request'].create({
            'template_id': template.id,
            'reference': f"ACH Signature for {self.crm_lead_id.name}",
            'request_item_ids': [(0, 0, {
                'partner_id': self.crm_lead_id.full_name.id,
                'role_id': 1,
            })],
            'reference' : "ACH Form.pdf",
            'subject' : "Signature Request - ACH Form.pdf"
        })

        # 5. Send the signature request
        # sign_request.action_sent()
        
        return {
            'type': 'ir.actions.act_window_close',
            'infos': {'sign_request_id': sign_request.id}
        }

                
                