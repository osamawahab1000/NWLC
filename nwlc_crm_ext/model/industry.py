from odoo import api , fields , models


class Industry(models.Model):
    _name="industry"

    name = fields.Char(string="Industry",required=False)



class IndustryLineId(models.Model):
    _name="industry.line.id"
    
    
    industry_crm_id = fields.Many2one('crm.lead',string="Industry Lines")
    name = fields.Char(string="Name")