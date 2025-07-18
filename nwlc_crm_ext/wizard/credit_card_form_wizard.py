from odoo import _,api,fields,models
from odoo.exceptions import UserError

import base64
class CreditCardWizard(models.TransientModel):
    _name = "credit.card"


    # name = fields.Char('crm.lead','name',string="Name")
    crm_lead_id = fields.Many2one('crm.lead', string="CRM Lead")

    full_name = fields.Char(string="Lead Name")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    street = fields.Char(string="Home Address")
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
    


    def print_credit_card(self):
        """Trigger the CRM Lead report printing."""
        self.ensure_one()  # Ensure only one wizard is active 
        self.crm_lead_id.account_type  = self.account_type 
        self.crm_lead_id.cardholder_name = self.cardholder_name 
        self.crm_lead_id.account_number = self.account_number 
        self.crm_lead_id.exp_date = self.exp_date 
        # data = {'data':self.crm_lead_id,'extra':self.no_10}
        return self.env.ref('nwlc_crm_ext.action_credit_card_form_template').report_action(self.crm_lead_id)
    

    def send_credit_card(self):
        """Generate the QWeb report and send it as an email attachment from the wizard."""

        # Ensure an email is provided
        if not self.email:
            raise UserError(_("Please provide an email address to send the report."))

        report  = self.env['ir.actions.report']._render_qweb_pdf("nwlc_crm_ext.action_credit_card_form_template",self.crm_lead_id.id)
        if not report:
            raise UserError(_("The report template was not found."))


            # Create an email attachment
        attachment = self.env['ir.attachment'].create({
            'name': f"Credit Card Form.pdf",
            'type': 'binary',
            'datas': base64.b64encode(report[0]),  # Encode PDF to Base64
            'res_model': 'crm.lead',
            'res_id': self.crm_lead_id.id,
            'mimetype': 'application/pdf',
        })

        # Prepare email values
        template = self.env.ref('nwlc_crm_ext.email_template_credit_card_form')  # Replace with your template ID
        template.send_mail(
            self.crm_lead_id.id,  # CRM Lead ID as the recipient
            force_send=True,  # Send immediately
            email_values={
                'email_to': self.email,
                'attachment_ids': [(4, attachment.id)],  # Add the generated PDF as an attachment
            }
        )

        return {'type': 'ir.actions.act_window_close'}
    
    
    def send_cc_form(self):
        if not self.crm_lead_id:
            raise UserError(_("No associated CRM lead found."))

        pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(
            "nwlc_crm_ext.action_credit_card_form_template", 
            self.crm_lead_id.id
        )

        if not pdf_content:
            raise UserError(_("Could not generate Credit Card form."))

        template = self.env.ref('nwlc_crm_ext.credit_card_form_template', raise_if_not_found=False)
        attachment = self.env['ir.attachment'].create({
            'name': f"{self.crm_lead_id.name}_cc_sign_Document.pdf",
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': 'sign.template',
        })
        if not template:
            template = self.env['sign.template'].create({
                'name': 'Credit Card Form Template',
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
        
        
        self.env['ir.attachment'].search([('id','=',attachment.id)]).write({
            'res_id': template.id,
        })


        sign_request = self.env['sign.request'].create({
            'template_id': template.id,
            'reference': f"Credit Card Signature for {self.crm_lead_id.name}",
            'request_item_ids': [(0, 0, {
                'partner_id': self.crm_lead_id.full_name.id,
                'role_id': 1,
            })],
            'reference' : "Credit Card Form.pdf",
            'subject' : "Signature Request - Credit Card Form.pdf"
        })

        return {
            'type': 'ir.actions.act_window_close',
            'infos': {'sign_request_id': sign_request.id}
        }

                
                