from odoo import api , fields , models
from odoo.exceptions import UserError




class CRMStage(models.Model):
    _inherit = "crm.stage"



    company_id = fields.Many2one(
            comodel_name='res.company',
            help="Define which company can select the multi-ledger in report filters. If none is provided, available for all companies",
            default=lambda self: self.env.company,
        )

    is_dead_sales = fields.Boolean('Is Dead Stage')