from odoo import api , fields , models


class AppSpecialist(models.Model):
    _name="app.specialist"

    name = fields.Char(string="App Specialist", required=False)


class AppSpecialistLineId(models.Model):
    _name="app.specialist.line.id"
    
    
    app_specialist_crm_id = fields.Many2one('crm.lead',string="App Specialist Line")
    name = fields.Char(string="Name")