from odoo import api , fields , models


class TransferredOutReason(models.Model):
    _name="transferred.out.reason"

    name = fields.Char(string="Transferred Out Reason")



class TransferredOutReasonLineId(models.Model):
    _name="transferred.out.reason.line.id"
    
    
    transferred_out_reason_crm_id = fields.Many2one('crm.lead',string="Transferred Out Reason Line")
    name = fields.Char(string="Name")