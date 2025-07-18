from odoo import _,models, fields, api
import random
import string
from datetime import datetime, timedelta
import logging
from odoo.exceptions import UserError, ValidationError
import requests
import json

_logger = logging.getLogger(__name__)
class AffiliatePartner(models.Model):
    _name = 'affiliate.api.access'
    
    
    affiliate_id = fields.Many2one('affiliate.partner', string='Parent')
    aff_id = fields.Char(string="Affiliate ID", related='affiliate_id.aff_id', store=True, readonly=True)
    api_key = fields.Char("Api Key")
    api_token = fields.Char("Api Token")
    message =  fields.Text("Message")


    @api.model
    def create(self, vals):
        vals['api_key'] = self.generate_api_key()
        return super(AffiliatePartner, self).create(vals)

    def generate_api_key(self, length=20):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))
    

    

    def generate_token(self):
        url = "https://nationwideloanconsultants.odoo.com/api/token/authenticate"
        
        payload = {
            "username": "yasir.siddiqui@affinitysuite.net",
            "password": "1234"
        }

        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        json_response = response.json()
        if response.status_code == 200:
            self['api_token'] = json_response['result'].get('token')
            self['message'] = json_response['result'].get('Message')
        else:
            self['message'] =  json_response['result'].get('Message')
