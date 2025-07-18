from odoo import models, fields, api
from collections import defaultdict
from odoo.exceptions import UserError, ValidationError

class Lenders(models.Model):
    _name = "lenders"
    _inherit = 'mail.thread'
    _description = "Lenders"

    company_id = fields.Many2one('res.company',default=lambda self: self.env.company.id,)
    creditor_status_ = fields.Many2one('creditors.status',string="Creditors Status")
    name = fields.Char(string="Lender Name",tracking=True)
    lender_update = fields.Char(string="Lender Update",tracking=True)
    lender_benefit = fields.Char(string="Lender Benefit",tracking=True)
    lender_description = fields.Text(string="Lender Description",tracking=True)
    how_to_secure  = fields.Char(string="How To Secure",tracking=True)
    how_to_present_lender  = fields.Char(string="How To Present Lender",tracking=True)
    static_note  = fields.Char(string="Static Note",tracking=True)
    phone  = fields.Char(string="Phone",tracking=True)
    status = fields.Selection(
        [
            ('active','Active'),
            ('inactive','Inactive')
        ],string="Status",
        tracking=True
    )
    web_address = fields.Char(string="Web Address",tracking=True)
    lender_support_email = fields.Char(string="Lender Support Email",tracking=True)






    