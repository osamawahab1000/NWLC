from odoo import _,api,fields,models
from odoo.exceptions import UserError
import base64



class DeadReasonWizard(models.TransientModel):
    _name = "dead.reason.wizard"
    _description = "Wizard for Dead Reason"

    dead_reason_id = fields.Many2one('dead.reason', string="Dead Reason", required=True)
    object_reason_id = fields.Many2one('object.reason', string="Objection Reason", required=True)
    lead_id = fields.Many2one('crm.lead', string="Lead")

    def apply_dead_reason(self):
        """Apply the selected dead reason to the lead."""
        self.ensure_one()
        # Update the lead with the selected reason and set stage to 'Dead'
        self.lead_id.dead_reason_id = self.dead_reason_id
        self.lead_id.object_reason_id = self.object_reason_id
        # dead_stage = self.env['crm.lead.stage'].search([('name', '=', 'Dead')], limit=1)
        dead_stage =  self.env.context.get('default_next_stage_id')
        if dead_stage:
            if self.lead_id.type =='opportunity':
                if self.dead_reason_id.id == 13: 
                    self.declined_by_All(self.lead_id)
                self.lead_id.stage_id = dead_stage  
            else:
                self.lead_id.lead_stage_id = dead_stage

        # next_stage = self.env.context.get('default_next_stage_id')
        # if next_stage:
        #     stage_rec = self.env['crm.stage'].browse(next_stage)
        #     if stage_rec.exists():
        #         self.lead_id.stage_id = stage_rec.id
        #         self.lead_id.lead_stage_id = stage_rec.id

        return {
            'type': 'ir.actions.client',
            'tag' : 'reload', 
        }
        

    def declined_by_All(self, record):
        for rec in self:
            if rec.company_id.id == 1:
                template = self.env.ref('nwlc_crm_ext.email_template_declined_by_all_partner')  # Replace with your template ID
                if not rec.email:
                    raise UserError("Customer Email has not provid")
                template.send_mail(
                    rec.id,  
                    force_send=True,  
                    email_values={
                        'email_to': rec.email,
                    }
                )
                
                template_aff = self.env.ref('nwlc_crm_ext.email_template_declined_by_all_affiliate')  # Replace with your template ID
                if not rec.source_ids.affiliate_email:
                    raise UserError("Affiliate Email has not provid")
                template_aff.send_mail(
                    rec.id,  
                    force_send=True,  
                    email_values={
                        'email_to': rec.source_ids.affiliate_email,
                    }
                )



    def no_contact_No_response(self):
        pass 


    def declined_Reason_Fee(self):
        pass
    