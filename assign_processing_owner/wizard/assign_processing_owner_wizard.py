# -*- coding: utf-8 -*-
from odoo import models, api, fields


class AssignProcessingOwner(models.Model):
    _name = 'assign.processing.owner'
    
    processing_owner = fields.Many2many('res.users', string='Processing Owner')

    # check sales person base on record id
    def chunkIt(self, seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
        return out
    
    # Assign salesperson methods
    def processing_owner_assign(self):
        leads = self.chunkIt(self._context.get('active_ids'), len(self.processing_owner.ids))
        counter = 0
        crm_lead_obj = self.env['crm.lead']
        for owner in self.processing_owner:
            crm_lead_rec = crm_lead_obj.browse(leads[counter])
            crm_lead_rec.with_context(mail_auto_subscribe_no_notify=1).write({'processing_owner': owner.id})
            counter += 1
        return True
