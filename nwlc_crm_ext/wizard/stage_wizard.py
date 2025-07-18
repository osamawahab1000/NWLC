from odoo import _,api,fields,models
from odoo.exceptions import UserError

import base64


class StageWizard(models.TransientModel):
    _name="stage.wizard"

    lead_id = fields.Many2one('crm.lead', string="Lead" )
    lead_stage_reason = fields.Selection(
        [
            ('think_about_it','Want To Think About It'),
            ('research','Do Some Research'),
            ('cannot_sign_csa','Cannot sign CSA at the moment'),
            ('setup_call_back','Setup call back time'),
            ('could_not_reach','Could not reach')
        ],
        string="Lead Stage Reason",
        tracking=True, 
        required=True
    ) 

    def send_email_Closed_Won(self , record):
        for rec in record:
            if rec.company_id.id == 1:
                template = self.env.ref('nwlc_crm_ext.email_template_close_and_won_partner')  # Replace with your template ID
                if not rec.email:
                    raise UserError("Customer Email has not provid")
                template.send_mail(
                    rec.id,  
                    force_send=True,  
                    email_values={
                        'email_to': rec.email,
                    }
                )
                
                template_aff = self.env.ref('nwlc_crm_ext.email_template_close_and_won_affiliate')  # Replace with your template ID
                if not rec.source_ids.affiliate_email:
                    raise UserError("Affiliate Email has not provid")
                template_aff.send_mail(
                    rec.id,  
                    force_send=True,  
                    email_values={
                        'email_to': rec.source_ids.affiliate_email,
                    }
                )



    def apply_reason(self):
        self.ensure_one()
        self.lead_id['stage_reason'] = self.lead_stage_reason

        next_stage = self.env.context.get('default_next_stage_id')
        if next_stage:
            if self.lead_id.type == 'opportunity':
                self.lead_id.write({'stage_id': next_stage})
                if self.lead_id.stage_id.is_won:
                    self.send_email_Closed_Won(self.lead_id)
            elif self.lead_id.type == 'lead':
                self.lead_id.write({'lead_stage_id': next_stage})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    