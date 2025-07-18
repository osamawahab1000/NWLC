from odoo import api , fields , models


class ObjectReason(models.Model):
    _name="object.reason"

    name = fields.Char(string="Objection Reason", required=False)



class ObjectReasonLineId(models.Model):
    _name="object.reason.line.id"
    
    
    object_reason_crm_id = fields.Many2one('crm.lead',string="Objection Reasons Line")
    name = fields.Char(string="Name")