from odoo import api , fields , models


class FlagsLead(models.Model):
    _name="flags.lead"

    company_id = fields.Many2one('res.company',default=lambda self: self.env.company.id,)
    name = fields.Char(string="Code")
    # flag_code_id = fields.Char(string="Code")
    flag_description = fields.Char(string="Description")

    
    
class FlagLineId(models.Model):
    _name="flags.line.id"
    
    
    crm_id = fields.Many2one('crm.lead',string="Flags")
    name = fields.Char(string="Name")
    flag_code = fields.Many2one('flags.lead',string="Code")
    flag_description = fields.Char(string="Description",related="flag_code.flag_description")
    