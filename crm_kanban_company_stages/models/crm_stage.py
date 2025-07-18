import pdb

from odoo import fields, models, api
from datetime import datetime


class Stage(models.Model):
    _inherit = "crm.stage"

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.model
    def get_stages_company(self):
        crm_list = {}
        crm_stages = self.env['crm.stage'].sudo().search_fetch(domain=[],field_names=['id', 'company_id'])
        for crm in crm_stages:
            crm_list.update({crm.id:crm.company_id.id})
        print('crm list:',crm_list)
        return crm_list
