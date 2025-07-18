from odoo import models, fields, api

class CRMLead(models.Model):
    _inherit = "crm.lead"

    custom_message_ids = fields.One2many(
        'mail.message', 'res_id',
        compute="_compute_custom_messages",
        string="Custom Chatter",
    )

    @api.depends('message_ids')
    def _compute_custom_messages(self):
        for lead in self:
            lead.custom_message_ids = lead.message_ids.filtered(lambda m: m.message_type == 'comment')
