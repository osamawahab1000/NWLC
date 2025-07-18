from odoo import _,models, fields, api

class AffiliatePartner(models.Model):
    _name = 'affiliate.partner'
    _description = 'Affiliate Partner'
    
    name = fields.Char(string="Name", required=True)
    affiliate_id = fields.Many2one('affiliate.partner', string='Parent')
    affiliate_manager = fields.Char(string="Affiliate Manager")
    affiliate_email = fields.Char(string="Affiliate Email")
    source_ids = fields.One2many('affiliate.partner', 'affiliate_id', string='Source')
    aff_id = fields.Char(string="Affiliate Id")
    

    @api.model
    def create(self, vals):
        """Automatically generate a reference number for new books."""
        if not vals.get('aff_id'):
            vals['aff_id'] = self.env['ir.sequence'].next_by_code('affiliate.partner')
        return super(AffiliatePartner, self).create(vals)