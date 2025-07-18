from odoo import _,api,fields,models
from odoo.exceptions import UserError

import base64
class BusinessGeneralAgreementWizard(models.TransientModel):
    _name = "business.general.agreement"


    # name = fields.Char('crm.lead','name',string="Name")
    crm_lead_id = fields.Many2one('crm.lead', string="CRM Lead")

    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    street = fields.Char(string="Home Address")
    yearly_income = fields.Float(string="Yearly Income")
    is_income_verifiable = fields.Selection(
        [
            ('yes','Yes'),
            ('no','No')
        ],string="Is Income Verifiable"
    )
    no_10 = fields.Char(string="Number 10")
    no_11 = fields.Char(string="Number 11")
    change_fee = fields.Char(string="Change Fee")
    
    


    def print_report_business(self):
        """Trigger the CRM Lead report printing."""
        self.ensure_one()  # Ensure only one wizard is active 
        self.crm_lead_id.is_income_verifiable = self.is_income_verifiable 
        self.crm_lead_id.no_10 = self.no_10 
        self.crm_lead_id.no_11 = self.no_11 
        self.crm_lead_id.change_fee = self.change_fee 
        # data = {'data':self.crm_lead_id,'extra':self.no_10}
        return self.env.ref('nwlc_crm_ext.action_business_general_agreement_template').report_action(self.crm_lead_id)
    
    
    


    def send_report_business(self):
        """Generate the QWeb report and send it as an email attachment from the wizard."""

        # Ensure an email is provided
        if not self.email:
            raise UserError(_("Please provide an email address to send the report."))

        report  = self.env['ir.actions.report']._render_qweb_pdf("nwlc_crm_ext.action_business_general_agreement_template",self.crm_lead_id.id)
        if not report:
            raise UserError(_("The report template was not found."))


            # Create an email attachment
        attachment = self.env['ir.attachment'].create({
            'name': f"Business General Agreement.pdf",
            'type': 'binary',
            'datas': base64.b64encode(report[0]),  # Encode PDF to Base64
            'res_model': 'crm.lead',
            'res_id': self.crm_lead_id.id,
            'mimetype': 'application/pdf',
        })

        # Prepare email values
        template = self.env.ref('nwlc_crm_ext.email_template_business_general_agreement')  # Replace with your template ID
        template.send_mail(
            self.crm_lead_id.id,  # CRM Lead ID as the recipient
            force_send=True,  # Send immediately
            email_values={
                'email_to': self.email,
                'attachment_ids': [(4, attachment.id)],  # Add the generated PDF as an attachment
            }
        )

        return {'type': 'ir.actions.act_window_close'}
    
    
    def send_business_agreement(self):
        if not self.crm_lead_id:
            raise UserError(_("No associated CRM lead found."))

        pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(
            "nwlc_crm_ext.action_business_general_agreement_template", 
            self.crm_lead_id.id
        )

        if not pdf_content:
            raise UserError(_("Could not generate Business General Agreement."))

        template = self.env.ref('nwlc_crm_ext.business_general_agreement_template', raise_if_not_found=False)
        attachment = self.env['ir.attachment'].create({
            'name': f"{self.crm_lead_id.name}_business_general_Document.pdf",
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': 'sign.template',
        })
        if not template:
            template = self.env['sign.template'].create({
                'name': 'Business General Agreement Template',
                'attachment_id': attachment.id,
                'sign_item_ids': [
                    (0, 0, {
                        'name': 'Customer Signature',
                        'type_id': self.env.ref('sign.sign_item_type_signature').id,
                        'required': True,
                        'page': 1,
                        'posX': 0.23,
                        'posY': 0.84,
                        'width': 0.28,
                        'height': 0.03,
                        'responsible_id':1,
                    }),
                ]
            })
        
        
        self.env['ir.attachment'].search([('id','=',attachment.id)]).write({
            'res_id': template.id,
        })


        sign_request = self.env['sign.request'].create({
            'template_id': template.id,
            'reference': f"Business General Agreement Signature for {self.crm_lead_id.name}",
            'request_item_ids': [(0, 0, {
                'partner_id': self.crm_lead_id.full_name.id,
                'role_id': 1,
            })],
            'reference' : "Business General Agreement.pdf",
            'subject' : "Signature Request - Business General Agreement.pdf"
        })

        return {
            'type': 'ir.actions.act_window_close',
            'infos': {'sign_request_id': sign_request.id}
        }