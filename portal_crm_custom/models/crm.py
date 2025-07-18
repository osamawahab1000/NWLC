# -*- coding: utf-8 -*-
import pdb

from odoo.tools import email_normalize
from odoo import api, fields, models, Command
from datetime import date


class CrmLead(models.Model):
    _name = "crm.lead"
    _inherit = ['crm.lead', 'portal.mixin', 'product.catalog.mixin', 'mail.thread', 'mail.activity.mixin']


    @api.model
    def create(self, vals):
        res = super(CrmLead, self).create(vals)
        return res

    def write(self, vals):
        res = super(CrmLead, self).write(vals)
        return res

    def _compute_access_url(self):
        super(CrmLead, self)._compute_access_url()
        for lead in self:
            lead.access_url = '/my/crm/lead/%s' % lead.id

    def _get_portal_return_action(self):
        """ Return the action used to display orders when returning from customer portal. """
        self.ensure_one()
        return self.env.ref('stock.action_picking_tree_ready')


class StockPickingMixin(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'portal.mixin']


class CrmStage(models.Model):
    _inherit = 'crm.stage'

class CrmStage(models.Model):
    _inherit = 'res.users'
    
    affiliate_id = fields.Many2one('affiliate.partner',string="Related Affiliate")

