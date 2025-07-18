from odoo import api , fields , models


class DeadSale(models.Model):
    _name="dead.sale"

    name = fields.Char(string="Dead Sale", required=False)


class DeadSaleLineId(models.Model):
    _name="dead.sale.line.id"
    
    
    dead_sale_crm_id = fields.Many2one('crm.lead',string="Dead Sale Line")
    name = fields.Char(string="Name")