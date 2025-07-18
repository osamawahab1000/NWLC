from odoo import models, fields

class CreditorsStatus(models.Model):
    _name = 'creditors.status'
    _inherit = ['mail.thread']  # Add this line to inherit mail thread

    company_id = fields.Many2one('res.company',default=lambda self: self.env.company.id,) 
    # creditor_status_crm_id = fields.Many2one('crm.lead',string="Creditors Status")  
    name = fields.Char(string="Status Name", required=True, tracking=True)