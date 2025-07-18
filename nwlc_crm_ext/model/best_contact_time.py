from odoo import api , fields , models


class BestContactTime(models.Model):
    _name="best.contact.time"

    name = fields.Char(string="Best Contact Time", required=False)


class BestContactTimeLineId(models.Model):
    _name="best.contact.time.line.id"
    
    
    best_contact_time_crm_id = fields.Many2one('crm.lead',string="Best Contact Time Line")
    name = fields.Char(string="Name")