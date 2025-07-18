from odoo import api , fields , models


class script(models.Model):
    _name="script"

    company_id = fields.Many2one('res.company',default=lambda self: self.env.company.id,)   
    name = fields.Char(string="Script")
    # flag_code_id = fields.Char(string="Code")
    description = fields.Text(string="Description")
