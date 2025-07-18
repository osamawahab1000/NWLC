from odoo import models, fields, api,_
from collections import defaultdict

class Creditors(models.Model):
    _name = "creditors"
    _inherit = 'mail.thread'
    _description = "Creditors"


    company_id = fields.Many2one('res.company',default=lambda self: self.env.company.id,) 
    creditor_crm_id = fields.Many2one('crm.lead',string="Creditors")  
    # creditor_status_ = fields.Many2one('creditors.status',string="Creditors Status")

    name = fields.Char(string="Creditor",tracking=True)
    lead_name = fields.Many2one('crm.lead',string="Lead Name",tracking=True)
    select_creditor = fields.Boolean(string="Select",tracking=True)
    portfolio_type = fields.Char(string="Portfolio Type",tracking=True)
    type = fields.Char(string="Type",tracking=True)
    account_number = fields.Char(string="Account Number",tracking=True)
    date_reported = fields.Date(string="Date Reported",tracking=True)
    credit_status = fields.Selection(
        [
            ('planned','Planned'),
            ('completed','Completed'),
            ('in_progress','In Progress'),
            ('aborted','Aborted')
        ],string="Status"
        ,tracking=True
    )
    effective_date = fields.Date(string="Effective Date",tracking=True)
    date_opened = fields.Date(string="Date Opened",tracking=True)
    client_effective_date = fields.Date(string="Client Effective Date",tracking=True)
    client_date_opened = fields.Date(string="Client Date Opened",tracking=True)
    credit_limit = fields.Float(string="Credit Limit",tracking=True)
    current_balance = fields.Float(string="Current Balance",tracking=True)
    term = fields.Char(string="Term",tracking=True)
    monthly_payment = fields.Float(string="Monthly Payment",tracking=True)
    high_credit = fields.Float(string="High Credit",tracking=True)
    status = fields.Char(string="Status",tracking=True)
    customer_number = fields.Char(string="Customer Number",tracking=True)




    def write(self, vals):
        
        creditor_initial_values = defaultdict(dict)

        tracking_fields = []
        for field_name in vals:
            field = self._fields[field_name]
            if not (hasattr(field, 'related') and field.related) and hasattr(field, 'tracking') and field.tracking:
                tracking_fields.append(field_name)
        fields_definition = self.env['creditors'].fields_get(tracking_fields)

        # Get initial values for each account
        for account in self:
            for field in tracking_fields:
                # Group initial values by partner_id
                creditor_initial_values[account][field] = account[field]

        res = super().write(vals)

        # Log changes to move lines on each move
        for creditor, initial_values in creditor_initial_values.items():
            tracking_value_ids = creditor._mail_track(fields_definition, initial_values)[1]
            if tracking_value_ids:
                msg = _("Creditor %s updated", creditor._get_html_link(title=f"#{creditor.name}"))
                creditor.creditor_crm_id._message_log(body=msg, tracking_value_ids=tracking_value_ids)
                if 'creditor_crm_id' in initial_values:  # notify previous partner as well
                    initial_values['creditor_crm_id']._message_log(body=msg, tracking_value_ids=tracking_value_ids)
        return res


    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for creditor in res:
            msg = _("Creditor %s created", creditor._get_html_link(title=f"#{creditor.name}"))
            creditor.creditor_crm_id._message_log(body=msg)
        return res


    def unlink(self):
        # EXTENDS base res.partner.bank
        for creditor in self:
            msg = _("Creditor %s deleted", creditor._get_html_link(title=f"#{creditor.name}"))
            creditor.creditor_crm_id._message_log(body=msg)
        return super().unlink()
