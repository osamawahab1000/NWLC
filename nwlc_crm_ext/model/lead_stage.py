# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Stage(models.Model):
    """ Model for case stages. This models the main stages of a document
        management flow. Main CRM objects (leads, opportunities, project
        issues, ...) will now use only stages, instead of state and stages.
        Stages are for example used to display the kanban view of records.
    """
    _name = "crm.lead.stage"
    _description = "CRM Lead Stages"
    _rec_name = 'name'
    _order = "sequence, name, id"

   

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    
    fold = fields.Boolean('Folded in Pipeline',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')
    is_duplicate_stage = fields.Boolean('Is Duplicate Stage')
    is_dead_stage = fields.Boolean('Is Dead Stage')
    is_dnc_stage = fields.Boolean('Is DNC Stage')
    
    # company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)


