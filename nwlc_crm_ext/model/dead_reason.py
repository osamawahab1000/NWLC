from odoo import api , fields , models


class DeadReason(models.Model):
    _name="dead.reason"

    name = fields.Char(string="Dead Reason", required=False)
    is_dead_lead = fields.Boolean(string="Is Dead Lead")
    is_unworkable_lead = fields.Boolean(string="Is Unworkable Lead")



class DeadReasonLineId(models.Model):
    _name="dead.reason.line.id"
    
    
    dead_reason_crm_id = fields.Many2one('crm.lead',string="Dead Reason Line")
    name = fields.Char(string="Name")