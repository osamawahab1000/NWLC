import json
from odoo import http
from odoo.http import request
from datetime import datetime,timedelta
from werkzeug.exceptions import BadRequest


from odoo import api, SUPERUSER_ID
import odoo

from odoo.exceptions import AccessError, UserError, AccessDenied


class CRMLeadController(http.Controller):
    
    @http.route('/api/token/authenticate', type='json', auth="none",methods=['POST'], csrf=False, save_session=False, cors="*")
    def get_token(self):
        try:
            byte_string = request.httprequest.data.decode('utf-8')
            data = json.loads(byte_string)
            username = data['username']
            password = data['password']
            credential = {'login': username, 'password': password, 'type': 'password'}
            user_id = request.session.authenticate(request.db, credential)
            if not user_id:
                return json.dumps({"error": "Invalid Username or Password."})
            
            env = request.env(user=request.env.user.browse(user_id['uid']))
            # env = request.env(user=request.env.user.browse(user_id))
            # return json.dumps({"uid": str(env)})
            expiration_date =  datetime.now() + timedelta(days=365)
        
            env['res.users.apikeys.description'].check_access_make_key()
            token = env['res.users.apikeys']._generate(None, username,expiration_date)
                
           
            
            return  {
                'username': username,
                'token': token,
                'Message': f'This token is only valid for 365 days and will expire on {expiration_date}',
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

        

    def authenticate_token(self, api_key,access_token):
   
        if not api_key:
            raise BadRequest(
                f"Please provide the API key in the header. {api_key}"
            )
        
        access_model = request.env['affiliate.api.access'].sudo().search([('api_key', '=', api_key)], limit=1)
        if not access_model:
            raise BadRequest(
                "This API key does not exist. Please enter the API key that was provided to you."
            )
            
        
        if not access_token:
            raise BadRequest('Access token missing')

        if access_token.startswith('Bearer '):
            access_token = access_token[7:]

        access_model = request.env['affiliate.api.access'].sudo().search([('api_token', '=', access_token),('api_key','=',api_key)], limit=1)
        user_id = request.env["res.users.apikeys"]._check_credentials(scope='odoo.plugin.outlook', key=access_token)
        if not user_id or not access_model:
            raise BadRequest('Access token invalid')

        # take the identity of the API key user
        request.update_env(user=user_id)

        # switch to the user context
        request.update_context(**request.env.user.context_get())




    @http.route('/api/create_crm_lead', type='json', auth='none', methods=['POST'], csrf=False)
    def create_crm_lead(self,token=None, **kwargs):
        try:
            api_key = request.httprequest.headers.get('api-key')  
            access_token = request.httprequest.headers.get('Authorization')


            data = json.loads(request.httprequest.data.decode('utf-8'))
            env = api.Environment(request.cr, 1,
                             {'active_test': False})
            # Validate required fields
            company_name = request.httprequest.headers.get('company')
            
            def authenticate_token(api_key,access_token):
        
                if not api_key:
                    raise BadRequest(
                        f"Please provide the API key in the header. {api_key}"
                    )
                
                access_model = request.env['affiliate.api.access'].sudo().search([('api_key', '=', api_key)], limit=1)
                if not access_model:
                    raise BadRequest(
                        "This API key does not exist. Please enter the API key that was provided to you."
                    )
                    
                
                if not access_token:
                    raise BadRequest('Access token missing')

                if access_token.startswith('Bearer '):
                    access_token = access_token[7:]

                access_model = request.env['affiliate.api.access'].sudo().search([('api_token', '=', access_token),('api_key','=',api_key)], limit=1)
                user_id = request.env["res.users.apikeys"]._check_credentials(scope='odoo.plugin.outlook', key=access_token)
                if not user_id or not access_model:
                    raise BadRequest('Access token invalid')

                # take the identity of the API key user
                request.update_env(user=user_id)

                # switch to the user context
                request.update_context(**request.env.user.context_get())

            authenticate_token(api_key,access_token)

            
            if not company_name or company_name.strip() not in ['NWLC', 'TBC', 'NWDR']:
                return {
                    'status': 'error',
                    'message': "Invalid or missing 'header' parameter. Only 'NWLC', 'TBC', or 'NWDR' are allowed, without any spaces. Please follow the exact format."
                }
            company_id = False
            if company_name == 'NWLC':
                company_id = 1
            elif company_name == 'NWDR':
                company_id = 4
            elif company_name == 'TBC':
                company_id = 3
            
            required_fields = [
                'Last_Name', 'First_Name', 'Email', 'Affiliate_Name', 'Lead_Source',
                'Loan_Desired', 'Credit_Score', 'Social_Security_Number', 'Mobile',
                'Residing_State', 'Street', 'Zip_Code', 'Affiliate_Sales_Rep',
                'Date_of_Birth', 'City', 'Gross_Annual_Income',
            ]
            missing_fields = [field for field in required_fields if field not in data or not data.get(field)]
            if missing_fields:
                return {'status': 'error', 'message': f'Missing fields: {", ".join(missing_fields)}'}

            # Fetch related fields from Odoo models
            state = request.env['res.country.state'].sudo().search([('code', '=', data.get('Residing_State'))], limit=1)
            lead_source = request.env['affiliate.partner'].sudo().search([('name', '=', data.get('Lead_Source'))], limit=1)
            affiliate = request.env['affiliate.partner'].sudo().search([('aff_id', '=', data.get('Affiliate_Name'))], limit=1)

            if not state:
                return {'status': 'error', 'message': f"Invalid Residing_State: {data.get('Residing_State')}"}
            if not lead_source:
                return {'status': 'error', 'message': f"Invalid Lead_Source: {data.get('Lead_Source')}"}
            if not affiliate:
                return {'status': 'error', 'message': f"Invalid Affiliate_Name: {data.get('Affiliate_Name')}"}

            # Parse Date_of_Birth
            try:
                date_of_birth = datetime.strptime(data.get('Date_of_Birth'), '%Y-%m-%d').date()
            except ValueError:
                return {'status': 'error', 'message': 'Invalid Date_of_Birth format. Use YYYY-MM-DD.'}

            # Prepare data for lead creation
            lead_data = {
                'first_name': data.get('First_Name'),
                'last_name': data.get('Last_Name'),
                'email': data.get('Email'),
                'requested_loan_amount': data.get('Loan_Desired'),
                'credit_score': data.get('Credit_Score'),
                'social_security_number': data.get('Social_Security_Number'),
                'mobile': data.get('Mobile'),
                'state_id': state.id,
                'street': data.get('Street'),
                'city': data.get('City'),
                'zip': data.get('Zip_Code'),
                'primary_gross_annual_income': data.get('Gross_Annual_Income'),
                'date_of_birth': date_of_birth,
                'source_ids': lead_source.id,  # Many2many field
                'affiliate_name': affiliate.id,
                'affiliate_id': affiliate.aff_id,
                'affiliate_sales_rep': data.get('Affiliate_Sales_Rep'),
                'user_id':2,
                'company_id':company_id,
            }

            partner = request.env['res.partner'].sudo().search([('name', '=', f"{data.get('First_Name')} {data.get('Last_Name')}")], limit=1)
            if not partner:
                partner_data = {
                    'name': f"{data.get('First_Name')} {data.get('Last_Name')}",
                    'email': data.get('Email'),
                    'phone': data.get('Mobile'),
                    'user_id':2,

                }
                partner = request.env['res.partner'].sudo().create(partner_data)
            lead_data['full_name'] = partner.id
            lead_data['name'] = partner.name
            # Create the CRM lead
            lead = env['crm.lead'].create(lead_data)
            return {'status': 'success', 'lead_id': lead.id, 'message': 'Lead created successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


