from odoo import models,api
from odoo.exceptions import UserError

class ResState(models.Model):
    _inherit = 'res.country.state'

    @api.depends('country_id')
    def _compute_display_name(self):
        res =  super(ResState, self)._compute_display_name()
        for record in self:
            record.display_name = f"{record.name} ({record.code})"
        return res