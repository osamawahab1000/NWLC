from odoo import api, fields, models, Command

class CrmLead(models.Model):
    _name = "crm.lead"
    _inherit = ['crm.lead', 'portal.mixin', 'product.catalog.mixin', 'mail.thread', 'mail.activity.mixin']


    @api.model
    def create(self, vals):
        res = super(CrmLead, self).create(vals)
        return res
    

    def crm_week(self):
        return "CRM Week"