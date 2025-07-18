from odoo import api , fields , models
from odoo.exceptions import UserError


class CRMTeamInherited(models.Model):
    _inherit = "crm.team"

    company = fields.Many2many('res.company',string="Company")