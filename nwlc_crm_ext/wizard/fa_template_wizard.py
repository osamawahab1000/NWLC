from odoo import _,api,fields,models
from odoo.exceptions import UserError

import base64
class FATemplateWizard(models.TransientModel):
    _name = "fa.template"


    # name = fields.Char('crm.lead','name',string="Name")
    crm_lead_id = fields.Many2one('crm.lead', string="CRM Lead")

    full_name = fields.Char(string="Customer Name")
    monthly_payment = fields.Char(string="Amount")
    date_sent = fields.Date(string="Date Sent")    
    email = fields.Char(string="Email")


    def print_fa_template(self):
        """Trigger the CRM Lead report printing."""
        self.ensure_one()  # Ensure only one wizard is active 
        self.crm_lead_id.monthly_payment  = self.monthly_payment 
        self.crm_lead_id.date_sent = self.date_sent 
        # self.crm_lead_id.bank_routing_number = self.bank_routing_number 
        # self.crm_lead_id.bank_account_number = self.bank_account_number 
        # self.crm_lead_id.date_funds_avail = self.date_funds_avail 
        # data = {'data':self.crm_lead_id,'extra':self.no_10}
        return self.env.ref('nwlc_crm_ext.action_fa_template').report_action(self.crm_lead_id)
    

    def send_fa_template(self):
        """Generate the QWeb report and send it as an email attachment from the wizard."""

        # Ensure an email is provided
        if not self.email:
            raise UserError(_("Please provide an email address to send the report."))

        report  = self.env['ir.actions.report']._render_qweb_pdf("nwlc_crm_ext.action_fa_template",self.crm_lead_id.id)
        if not report:
            raise UserError(_("The report template was not found."))


            # Create an email attachment
        attachment = self.env['ir.attachment'].create({
            'name': f"FA.pdf",
            'type': 'binary',
            'datas': base64.b64encode(report[0]),  # Encode PDF to Base64
            'res_model': 'crm.lead',
            'res_id': self.crm_lead_id.id,
            'mimetype': 'application/pdf',
        })

        # Prepare email values
        template = self.env.ref('nwlc_crm_ext.email_template_fa_template')  # Replace with your template ID
        template.send_mail(
            self.crm_lead_id.id,  # CRM Lead ID as the recipient
            force_send=True,  # Send immediately
            email_values={
                'email_to': self.email,
                'attachment_ids': [(4, attachment.id)],  # Add the generated PDF as an attachment
            }
        )

        return {'type': 'ir.actions.act_window_close'}