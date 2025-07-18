# from odoo.http import request
# from odoo import fields, models, http, SUPERUSER_ID, _
# from odoo.exceptions import UserError
# import ast

# from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
# from datetime import datetime


# class crmSalesDashboard(models.Model):
#     _inherit="crm.lead"


#     def get_total_crm_lead(self):


#         user_data = request.env['crm.lead'].read_group(
#             domain=[('type', '=', 'lead')],
#             fields=['affiliate_name'],
#             groupby=['affiliate_name']
#         )

#         result = []

#         for user in user_data:
#             total_live_leads_count = 0
#             total_portal_leads_count = 0
#             total_live_duplicates_count = 0  # Count for duplicates in live leads
#             total_portal_duplicates_count = 0  # Count for duplicates in portal leads
#             total_live_dnmc_lead_count = 0
#             total_portal_dnmc_lead_count = 0
#             total_live_workable_count = 0
#             total_portal_workable_count = 0 
#             total_workable_count = 0
#             total_live_declined_lead_count = 0
#             total_portal_declined_lead_count = 0
#             total_live_dnc_lead_count = 0
#             total_portal_dnc_lead_count = 0
#             total_live_transferred_lead_count = 0 
#             total_portal_transferred_lead_count = 0 
#             total_live_no_contact_lead_count = 0
#             total_portal_no_contact_lead_count = 0
#             total_live_no_response_lead_count = 0 
#             total_portal_no_response_lead_count = 0
#             total_live_deal_lead_count = 0
#             total_portal_deal_lead_count = 0
#             total_subprime_lead_count = 0
#             total_prime_lead_count = 0 
#             total_subprime_dup_lead_count = 0
#             total_prime_dup_lead_count = 0 
#             total_subprime_dnmc_lead_count = 0
#             total_prime_dnmc_lead_count = 0 
#             total_subprime_workable_lead_count = 0
#             total_prime_workable_lead_count = 0 
#             total_subprime_declined_lead_count = 0
#             total_prime_declined_lead_count = 0 
#             total_subprime_dnc_lead_count = 0
#             total_prime_dnc_lead_count = 0 
#             total_prime_transferred_lead_count = 0
#             total_subprime_transferred_lead_count = 0
#             total_prime_no_contact_lead_count = 0
#             total_subprime_no_contact_lead_count = 0
#             total_prime_no_response_lead_count = 0
#             total_subprime_no_response_lead_count = 0

#             user_id = user.get('affiliate_name') and user['affiliate_name'][0] or False
#             user_name = user.get('affiliate_name') and user['affiliate_name'][1] or 'Undefined'

#             # 🔹 Step 2: Ab har user ke andar stage-wise grouping karni hai
#             stage_data = request.env['crm.lead'].read_group(
#                 domain=[('type', '=', 'lead'), ('affiliate_name', '=', user_id)],
#                 fields=['lead_stage_id'],
#                 groupby=['lead_stage_id']
#             )

#             user_lead_data = []
#             for stage in stage_data:
#                 stage_id = stage.get('lead_stage_id') and stage['lead_stage_id'][0] or False
#                 stage_name = stage.get('lead_stage_id') and stage['lead_stage_id'][1] or 'Undefined'

#                 lead_domain = [('type', '=', 'lead'), ('user_id', '=', user_id)]
#                 if stage_id:
#                     lead_domain.append(('lead_stage_id', '=', stage_id))
                
#                 total_lead_count = request.env['crm.lead'].search_count(lead_domain)
#                 lead = request.env['crm.lead'].search(lead_domain, limit=None)

#                 # Filter leads into live and portal
#                 live_leads = lead.filtered(lambda lead: lead.live_transfer)
#                 portal_leads = lead.filtered(lambda lead: not lead.live_transfer)

#                 live_leads_count = len(live_leads)
#                 portal_leads_count = len(portal_leads)

#                 # Calculate duplicates in live and portal leads
#                 duplicate_stage_ids = request.env['crm.lead.stage'].search([('is_duplicate_stage', '=', True)]).ids
#                 live_duplicates = live_leads.filtered(lambda lead: lead.lead_stage_id.id in duplicate_stage_ids)
#                 portal_duplicates = portal_leads.filtered(lambda lead: lead.lead_stage_id.id in duplicate_stage_ids)

#                 live_duplicates_count = len(live_duplicates)
#                 portal_duplicates_count = len(portal_duplicates)


#                 # Calculate dnmc in live and portal leads
#                 live_dnmc_lead = live_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.object_reason_id.id == 3)
#                 portal_dnmc_lead = portal_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.object_reason_id.id == 3)

#                 live_dnmc_lead_count = len(live_dnmc_lead)
#                 portal_dnmc_lead_count = len(portal_dnmc_lead)

#                 #calculate live workable and portal workable

#                 live_workable = live_leads_count -(live_duplicates_count + live_dnmc_lead_count)
#                 portal_workable = portal_leads_count -(portal_duplicates_count + portal_dnmc_lead_count)
                
#                 #total workable
#                 total_workable =  live_workable + portal_workable
                
#                 #total live and portal declined offer

#                 live_declined_lead = live_leads.filtered(
#                 lambda lead: lead.lead_stage_id.id == 5 and lead.dead_reason_id and lead.dead_reason_id.id == 1
#                 )
#                 portal_declined_lead = portal_leads.filtered(
#                     lambda lead: lead.lead_stage_id.id == 5 and lead.dead_reason_id and lead.dead_reason_id.id == 1
#                 )

#                 live_declined_lead_count = len(live_declined_lead)
#                 portal_declined_lead_count = len(portal_declined_lead)
                
#                 #live and portal dnc Leads
#                 dnc_stage_ids = request.env['crm.lead.stage'].search([('is_dnc_stage', '=', True)]).ids
#                 live_dnc_lead = live_leads.filtered(lambda lead: lead.lead_stage_id.id in dnc_stage_ids)
#                 portal_dnc_lead = portal_leads.filtered(lambda lead: lead.lead_stage_id.id in dnc_stage_ids)

#                 live_dnc_lead_count = len(live_dnc_lead)
#                 portal_dnc_lead_count = len(portal_dnc_lead)

#                 # live and portal transferred out leads
#                 live_transferred_lead = live_leads.filtered(lambda lead: lead.lead_stage_id.id == 10)    
#                 portal_transferred_lead = portal_leads.filtered(lambda lead: lead.lead_stage_id.id == 10)    

#                 live_transferred_lead_count = len(live_transferred_lead)
#                 portal_transferred_lead_count = len(portal_transferred_lead)

#                 #live and portal no contact leads
#                 live_no_contact_lead = live_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 3)
#                 portal_no_contact_lead = portal_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 3)

#                 live_no_contact_lead_count = len(live_no_contact_lead)
#                 portal_no_contact_lead_count = len(portal_no_contact_lead)    
                
#                 #live and portal no reponse leads

#                 live_no_response_lead = live_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 2)
#                 portal_no_response_lead = portal_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 2)

#                 live_no_response_lead_count = len(live_no_response_lead)
#                 portal_no_response_lead_count = len(portal_no_response_lead)
                
#                 #live and portal leads Converted (Deals)
#                 live_deal_lead = live_leads.filtered(lambda lead:lead.converted_lead == True and lead.lead_stage_id.id not in [5,7,9])
#                 portal_deal_lead = portal_leads.filtered(lambda lead:lead.converted_lead == True and lead.lead_stage_id.id not in [5,7,9])

#                 live_deal_lead_count = len(live_deal_lead)
#                 portal_deal_lead_count = len(portal_deal_lead)

#                 #Prime and Subprime lead
#                 # subprime_lead = lead.filtered(lambda lead:lead.loan_type == 'sub_prime' and lead.lead_stage_id.id not in [5,7,9])
#                 # prime_lead = lead.filtered(lambda lead:lead.loan_type != 'sub_prime' and lead.lead_stage_id.id not in [5,7,9])
#                 subprime_lead = lead.filtered(lambda lead:lead.loan_type == 'sub_prime')
#                 prime_lead = lead.filtered(lambda lead:lead.loan_type != 'sub_prime')
                
#                 subprime_lead_count = len(subprime_lead)
#                 prime_lead_count = len(prime_lead)
                
#                 #Prime and Subprime duplicates lead
#                 subprime_dup_lead = lead.filtered(lambda lead:lead.loan_type == 'sub_prime' and lead.lead_stage_id.id in duplicate_stage_ids)
#                 prime_dup_lead = lead.filtered(lambda lead:lead.loan_type != 'sub_prime' and lead.lead_stage_id.id in duplicate_stage_ids)
                
#                 subprime_dup_lead_count = len(subprime_dup_lead)
#                 prime_dup_lead_count = len(prime_dup_lead)
                
#                 #Prime and Subprime dnmc lead
#                 subprime_dnmc_lead = lead.filtered(lambda lead:lead.loan_type == 'sub_prime' and lead.object_reason_id.id == 3)
#                 prime_dnmc_lead = lead.filtered(lambda lead:lead.loan_type != 'sub_prime' and lead.object_reason_id.id == 3)
                
#                 subprime_dnmc_lead_count = len(subprime_dnmc_lead)
#                 prime_dnmc_lead_count = len(prime_dnmc_lead)
                
#                 #Prime and Subprime Workable lead

#                 subprime_workable_lead_ids = []

#                 for i in subprime_lead:
#                     subprime_workable_lead_ids.append(i.id)
#                 for j in subprime_dup_lead:
#                     if j.id in subprime_workable_lead_ids:
#                         subprime_workable_lead_ids.remove(j.id)
#                 for k in subprime_dnmc_lead:
#                     if k.id in subprime_workable_lead_ids:
#                         subprime_workable_lead_ids.remove(k.id)
                
                
#                 prime_workable_lead_ids = []

#                 for i in prime_lead:
#                     prime_workable_lead_ids.append(i.id)
#                 for j in prime_dup_lead:
#                     if j.id in prime_workable_lead_ids:
#                         prime_workable_lead_ids.remove(j.id)
#                 for k in prime_dnmc_lead:
#                     if k.id in prime_workable_lead_ids:
#                         prime_workable_lead_ids.remove(k.id)
                
#                 subprime_workable_leads = self.env['crm.lead'].search([('id','in',subprime_workable_lead_ids)])
#                 prime_workable_leads = self.env['crm.lead'].search([('id','in',prime_workable_lead_ids)])

#                 prime_workable_leads_count = len(prime_workable_lead_ids)
#                 subprime_workable_leads_count = len(subprime_workable_lead_ids)

#                 #Prime and Subprime Declined lead
#                 prime_declined_lead = prime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 1)
#                 subprime_declined_lead = subprime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 1)
                
#                 prime_declined_lead_count = len(prime_declined_lead)
#                 subprime_declined_lead_count = len(subprime_declined_lead)

#                 #Prime and Subprime Dnc lead
#                 prime_dnc_lead = prime_workable_leads.filtered(lambda lead: lead.lead_stage_id.id in dnc_stage_ids)
#                 subprime_dnc_lead = subprime_workable_leads.filtered(lambda lead: lead.lead_stage_id.id in dnc_stage_ids)

#                 prime_dnc_lead_count = len(prime_dnc_lead)
#                 subprime_dnc_lead_count = len(subprime_dnc_lead)

#                 # Prime and Subprime transferred out leads
#                 prime_transferred_lead = prime_workable_leads.filtered(lambda lead: lead.lead_stage_id.id == 10)    
#                 subprime_transferred_lead = subprime_workable_leads.filtered(lambda lead: lead.lead_stage_id.id == 10)    

#                 prime_transferred_lead_count = len(prime_transferred_lead)
#                 subprime_transferred_lead_count = len(subprime_transferred_lead)

#                 #live and portal no contact leads
#                 prime_no_contact_lead = prime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 3)
#                 subprime_no_contact_lead = subprime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 3)

#                 prime_no_contact_lead_count = len(prime_no_contact_lead)
#                 subprime_no_contact_lead_count = len(subprime_no_contact_lead)    
                
#                 #live and portal no reponse leads

#                 prime_no_response_lead = prime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 2)
#                 subprime_no_response_lead = subprime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 2)

#                 prime_no_response_lead_count = len(prime_no_response_lead)
#                 subprime_no_response_lead_count = len(subprime_no_response_lead)

#                 # Update totals
#                 total_live_leads_count += live_leads_count
#                 total_portal_leads_count += portal_leads_count
#                 total_live_duplicates_count += live_duplicates_count
#                 total_portal_duplicates_count += portal_duplicates_count
#                 total_live_dnmc_lead_count += live_dnmc_lead_count 
#                 total_portal_dnmc_lead_count += portal_dnmc_lead_count 
#                 total_live_workable_count += live_workable
#                 total_portal_workable_count += portal_workable
#                 total_workable_count += total_workable
#                 total_live_declined_lead_count += live_declined_lead_count
#                 total_portal_declined_lead_count += portal_declined_lead_count
#                 total_live_dnc_lead_count += live_dnc_lead_count
#                 total_portal_dnc_lead_count += portal_dnc_lead_count
#                 total_live_transferred_lead_count += live_transferred_lead_count
#                 total_portal_transferred_lead_count += portal_transferred_lead_count
#                 total_live_no_contact_lead_count += live_no_contact_lead_count
#                 total_portal_no_contact_lead_count += portal_no_contact_lead_count
#                 total_live_no_response_lead_count += live_no_response_lead_count
#                 total_portal_no_response_lead_count += portal_no_response_lead_count
#                 total_live_deal_lead_count += live_deal_lead_count
#                 total_portal_deal_lead_count += portal_deal_lead_count
#                 total_subprime_lead_count += subprime_lead_count
#                 total_prime_lead_count += prime_lead_count
#                 total_subprime_dup_lead_count += subprime_dup_lead_count
#                 total_prime_dup_lead_count += prime_dup_lead_count
#                 total_subprime_dnmc_lead_count += subprime_dnmc_lead_count
#                 total_prime_dnmc_lead_count += prime_dnmc_lead_count
#                 total_prime_workable_lead_count += prime_workable_leads_count
#                 total_subprime_workable_lead_count += subprime_workable_leads_count
#                 total_prime_declined_lead_count += prime_declined_lead_count
#                 total_subprime_declined_lead_count += subprime_declined_lead_count
#                 total_prime_dnc_lead_count += prime_dnc_lead_count
#                 total_subprime_dnc_lead_count += subprime_dnc_lead_count
#                 total_prime_transferred_lead_count += prime_transferred_lead_count
#                 total_subprime_transferred_lead_count += subprime_transferred_lead_count
#                 total_prime_no_contact_lead_count += prime_no_contact_lead_count
#                 total_subprime_no_contact_lead_count += subprime_no_contact_lead_count
#                 total_prime_no_response_lead_count += prime_no_response_lead_count
#                 total_subprime_no_response_lead_count += subprime_no_response_lead_count

#                 user_lead_data.append({
#                     'lead_stage_id': stage_id or 'No Stage',
#                     'lead_stage_name': stage_name,  
#                     'data': lead.ids,
#                 })

#             result.append({
#                 'user_id': user_id or 'No User Assigned',
#                 'user_name': user_name,
#                 'stages': user_lead_data,
#                 'total_live_lead': total_live_leads_count,
#                 'total_portal_lead': total_portal_leads_count,
#                 'total_live_duplicate': total_live_duplicates_count,  # Total live duplicates
#                 'total_portal_duplicate': total_portal_duplicates_count,  # Total portal duplicates
#                 'total_live_dnmc_lead' : total_live_dnmc_lead_count,
#                 'total_portal_dnmc_lead' : total_portal_dnmc_lead_count,
#                 'total_live_workable' : total_live_workable_count,
#                 'total_portal_workable' : total_portal_workable_count,
#                 'total_workable_lead' : total_workable_count,
#                 'total_live_declined_lead': total_live_declined_lead_count,
#                 'total_portal_declined_lead': total_portal_declined_lead_count,
#                 'total_live_dnc_lead': total_live_dnc_lead_count,
#                 'total_portal_dnc_lead': total_portal_dnc_lead_count,
#                 'total_live_transferred_lead': total_live_transferred_lead_count,
#                 'total_portal_transferred_lead': total_portal_transferred_lead_count,
#                 'total_live_no_contact_lead': total_live_no_contact_lead_count,
#                 'total_portal_no_contact_lead': total_portal_no_contact_lead_count,
#                 'total_live_no_response_lead': total_live_no_response_lead_count,
#                 'total_portal_no_response_lead': total_portal_no_response_lead_count,
#                 'total_live_deal_lead': total_live_deal_lead_count,
#                 'total_portal_deal_lead': total_portal_deal_lead_count,
#                 'total_prime_lead' : total_prime_lead_count,
#                 'total_subprime_lead' : total_subprime_lead_count,
#                 'total_prime_dup_lead' : total_prime_dup_lead_count,
#                 'total_subprime_dup_lead' : total_subprime_dup_lead_count,
#                 'total_prime_dnmc_lead' : total_prime_dnmc_lead_count,
#                 'total_subprime_dnmc_lead' : total_subprime_dnmc_lead_count,
#                 'total_subprime_workable_lead' : total_subprime_workable_lead_count,
#                 'total_prime_workable_lead' : total_prime_workable_lead_count,
#                 'total_subprime_declined_lead' : total_subprime_declined_lead_count,
#                 'total_prime_declined_lead' : total_prime_declined_lead_count,
#                 'total_subprime_dnc_lead' : total_subprime_dnc_lead_count,
#                 'total_prime_dnc_lead' : total_prime_dnc_lead_count,
#                 'total_subprime_transferred_lead' : total_subprime_transferred_lead_count,
#                 'total_prime_transferred_lead' : total_prime_transferred_lead_count,
#                 'total_subprime_no_contact_lead' : total_subprime_no_contact_lead_count,
#                 'total_prime_no_contact_lead' : total_prime_no_contact_lead_count,
#                 'total_subprime_no_response_lead' : total_subprime_no_response_lead_count,
#                 'total_prime_no_response_lead' : total_prime_no_response_lead_count,
#             })

#         return result


# class CRMSalesDashboardController(http.Controller):


#     @http.route('/crm_sales_dashboard/get_total_crm_leads', type='json', auth='user')
#     def get_total_crm_leads(self):
#         """
#         Call the `get_total_leads` function from the `crm.lead` model.
#         """
#         # Context se date_domain fetch karo agar zaroori ho
#         # date_domain = get_today_date_domain()  # Tum yaha filter add kar sakte ho
        
#         # Model function call karna
#         # total_leads_data = request.env['crm.lead'].get_total_leads()
#         total_leads_data_new = request.env['crm.lead'].get_total_crm_lead()

#         # Response return karna JSON format me
#         return {'get_total_leads_new':total_leads_data_new}