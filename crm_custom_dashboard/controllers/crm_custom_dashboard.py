# -*- coding: utf-8 -*-
from odoo.addons.portal.controllers import portal as payment_portal
from odoo.addons.portal_crm_custom.controllers import portal as CustomerPortal 
from odoo.http import request
from odoo import fields, models, http, SUPERUSER_ID, _
from odoo.exceptions import UserError
import ast

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from datetime import datetime

def get_today_date_domain():
    today = datetime.today().strftime('%Y-%m-%d')
    return [
        ('create_date', '>=', today + " 00:00:00"), 
        ('create_date', '<=', today + " 23:59:59")
    ]


def get_converted_date_domain():
    today = datetime.today().strftime('%Y-%m-%d')
    return [
        ('converted_lead_date', '>=', today + " 00:00:00"), 
        ('converted_lead_date', '<=', today + " 23:59:59")
    ]

class CrmCustomDashboard(models.Model):
    _inherit="crm.lead"


        # (1st Dashboard) Daily Count Dashboard Starting

    def get_open_leads(self,date_domain):
        # date_domain = get_today_date_domain()
        stage_data = request.env['crm.lead'].read_group(
            domain=[('type', '=', 'lead')] + date_domain,
            fields=['lead_stage_id'],
            groupby=['lead_stage_id']
        )

        result = []

        for stage in stage_data:
            stage_id = stage['lead_stage_id'][0] if stage['lead_stage_id'] else None
            stage_name = stage['lead_stage_id'][1] if stage['lead_stage_id'] else 'Undefined'

            if stage_id:
                leads_domain = [('type', '=', 'lead'), ('lead_stage_id', '=', stage_id)] + date_domain
                lead_count = request.env['crm.lead'].search_count(leads_domain)
                leads = request.env['crm.lead'].search(leads_domain, limit=None)  # 🔥 Fetch all records

                result.append({
                    'stage_name': stage_name,
                    'count': lead_count,  # ✅ Ye total count dikhayega
                    'data': leads.ids,    # ✅ Ab sabhi IDs milengi
                })

        return result
    
    

    def get_duplicate_stage(self, date_domain):

        date_domain = get_today_date_domain()
        """Fetch duplicate leads count in real-time"""
        
        dup_stage_ids = request.env['crm.lead.stage'].search([('is_duplicate_stage', '=', True)]).ids

        duplicate_leads = request.env['crm.lead'].search(
            [('lead_stage_id', 'in', dup_stage_ids),('type','=','lead')]+ date_domain 
            
        )

        return [{
            'stage_name': 'Duplicate Leads',
            'count': len(duplicate_leads),
            'data': duplicate_leads.ids,
        }]

    def get_dnmc(self, date_domain):
        """Fetch DNMC leads count in real-time"""
        
        # request.env.cr.execute("SELECT id FROM crm_lead WHERE object_reason_id = 3 and type = 'lead'")
        # dnmc_leads_ids = [row[0] for row in request.env.cr.fetchall()]
        dnmc_leads_ids = request.env['crm.lead'].search([
            ('lead_stage_id','=',5),
            ('object_reason_id','=',19),
            ('type','=','lead')]
            + date_domain)

        dnmc_leads = request.env['crm.lead'].browse(dnmc_leads_ids)

        return [{
            'stage_name': 'Did Not Meet Criteria',
            'count': len(dnmc_leads),
            'data': dnmc_leads_ids.ids,
        }]

    def get_converted_leads(self,date_domain):
        """Fetch Converted Leads count in real-time"""
        date_domain = get_converted_date_domain()
        converted_leads = request.env['crm.lead'].sudo().search([
            ('converted_lead', '=', True),
            ('type', '=', 'opportunity')
        ] + date_domain)

        return [{
            'stage_name': 'Converted Leads',
            'count': len(converted_leads),
            'data': converted_leads.ids,
        }]


    def get_dead_declined(self, date_domain):
        """Fetch Dead declined offer leads count in real-time"""
        
        # request.env.cr.execute("SELECT id FROM crm_lead WHERE dead_reason_id = 1 and type = 'lead'")
        # dead_leads_ids = [row[0] for row in request.env.cr.fetchall()]
        dead_leads_ids = request.env['crm.lead'].search([
            ('lead_stage_id','=',5),
            ('dead_reason_id','=',1),
            ('type','=','lead')
            ] + date_domain)
        dead_leads = request.env['crm.lead'].browse(dead_leads_ids)

        return [{
            'stage_name': 'Dead Decline Offers',
            'count': len(dead_leads),
            'data': dead_leads_ids.ids,
        }]
        # (1st Dashboard) Daily Count Dashboard Ending


    def get_consultation_processing(self,date_domain=None):
        date_domain = get_converted_date_domain()
        consultation_processing_ids = request.env['crm.lead'].search([
            ('stage_id','=',28),
            ('type','=','opportunity')
            ] + date_domain)
        consultation_processing = request.env['crm.lead'].browse(consultation_processing_ids)

        return [{
            'stage_name': 'Consultation',
            'count': len(consultation_processing),
            'data': consultation_processing_ids.ids,
        }]
    
    
    def get_application_in_process(self,date_domain=None):
        date_domain = get_converted_date_domain()
        application_in_process_ids = request.env['crm.lead'].search([
            ('stage_id','=',6),
            ('type','=','opportunity')
            ] + date_domain)
        application_in_process = request.env['crm.lead'].browse(application_in_process_ids)

        return [{
            'stage_name': 'Application In Process',
            'count': len(application_in_process),
            'data': application_in_process_ids.ids,
        }]

    
    def get_freeze_processing(self,date_domain=None):
        date_domain = get_converted_date_domain()
        freeze_processing_ids = request.env['crm.lead'].search([
            ('stage_id','=',8),
            ('type','=','opportunity')
            ] + date_domain)
        freeze_processing = request.env['crm.lead'].browse(freeze_processing_ids)

        return [{
            'stage_name': 'Freeze',
            'count': len(freeze_processing),
            'data': freeze_processing_ids.ids,
        }]
    
    
    def get_processing(self,date_domain=None):
        date_domain = get_converted_date_domain()
        processing_ids = request.env['crm.lead'].search([
            ('stage_id','=',9),
            ('type','=','opportunity')
            ] + date_domain)
        processing = request.env['crm.lead'].browse(processing_ids)

        return [{
            'stage_name': 'Freeze',
            'count': len(processing),
            'data': processing_ids.ids,
        }]
    
    
    def get_add_lender(self,date_domain=None):
        date_domain = get_converted_date_domain()
        add_lender_ids = request.env['crm.lead'].search([
            ('stage_id','=',10),
            ('type','=','opportunity')
            ] + date_domain)
        add_lender = request.env['crm.lead'].browse(add_lender_ids)

        return [{
            'stage_name': 'Freeze',
            'count': len(add_lender),
            'data': add_lender_ids.ids,
        }]


    def get_submitting_docs(self,date_domain=None):
        date_domain = get_converted_date_domain()
        submitting_docs_ids = request.env['crm.lead'].search([
            ('stage_id','=',11),
            ('type','=','opportunity')
            ] + date_domain)
        submitting_docs = request.env['crm.lead'].browse(submitting_docs_ids)

        return [{
            'stage_name': 'Freeze',
            'count': len(submitting_docs),
            'data': submitting_docs_ids.ids,
        }]


    def get_signed_closing_docs(self,date_domain=None):
        date_domain = get_converted_date_domain()
        signed_closing_docs_ids = request.env['crm.lead'].search([
            ('stage_id','=',12),
            ('type','=','opportunity')
            ] + date_domain)
        signed_closing_docs = request.env['crm.lead'].browse(signed_closing_docs_ids)

        return [{
            'stage_name': 'Freeze',
            'count': len(signed_closing_docs),
            'data': signed_closing_docs_ids.ids,
        }]


    def get_pending_processing(self,date_domain=None):
        date_domain = get_converted_date_domain()
        pending_processing_ids = request.env['crm.lead'].search([
            ('stage_id','=',5),
            ('type','=','opportunity')
            ] + date_domain)
        pending_processing = request.env['crm.lead'].browse(pending_processing_ids)

        return [{
            'stage_name': 'Freeze',
            'count': len(pending_processing),
            'data': pending_processing_ids.ids,
        }]



        # (2nd Dashboard) Owner Dashboard Starting

    def get_total_leads_new(self):
        # 🔹 Step 1: Pehle user_id ke basis par grouping
        user_data = request.env['crm.lead'].read_group(
            domain=[('type', '=', 'lead')],
            fields=['user_id'],
            groupby=['user_id']
        )
        

        result = []
        

        for user in user_data:
            total_live_leads_count = 0
            total_portal_leads_count = 0
            total_live_duplicates_count = 0  # Count for duplicates in live leads
            total_portal_duplicates_count = 0  # Count for duplicates in portal leads
            total_live_dnmc_lead_count = 0
            total_portal_dnmc_lead_count = 0
            total_live_workable_count = 0
            total_portal_workable_count = 0 
            total_workable_count = 0
            total_live_declined_lead_count = 0
            total_portal_declined_lead_count = 0
            total_live_dnc_lead_count = 0
            total_portal_dnc_lead_count = 0
            total_live_transferred_lead_count = 0 
            total_portal_transferred_lead_count = 0 
            total_live_no_contact_lead_count = 0
            total_portal_no_contact_lead_count = 0
            total_live_no_response_lead_count = 0 
            total_portal_no_response_lead_count = 0
            total_live_deal_lead_count = 0
            total_portal_deal_lead_count = 0
            total_subprime_lead_count = 0
            total_prime_lead_count = 0 
            total_subprime_dup_lead_count = 0
            total_prime_dup_lead_count = 0 
            total_subprime_dnmc_lead_count = 0
            total_prime_dnmc_lead_count = 0 
            total_subprime_workable_lead_count = 0
            total_prime_workable_lead_count = 0 
            total_subprime_declined_lead_count = 0
            total_prime_declined_lead_count = 0 
            total_subprime_dnc_lead_count = 0
            total_prime_dnc_lead_count = 0 
            total_prime_transferred_lead_count = 0
            total_subprime_transferred_lead_count = 0
            total_prime_no_contact_lead_count = 0
            total_subprime_no_contact_lead_count = 0
            total_prime_no_response_lead_count = 0
            total_subprime_no_response_lead_count = 0


            live_leads_ids = []
            portal_leads_ids = []
            combined_leads_ids = []
            live_duplicates_ids = []
            portal_duplicates_ids = []
            live_dnmc_lead_ids = []
            portal_dnmc_lead_ids = []
            live_workable_ids = []
            portal_workable_ids = []
            total_workable_ids = []
            live_declined_lead_ids = []
            portal_declined_lead_ids = []
            live_dnc_lead_ids = []
            portal_dnc_lead_ids = []
            live_transferred_lead_ids = []
            portal_transferred_lead_ids = []
            live_no_contact_lead_ids = []
            portal_no_contact_lead_ids = []
            live_no_response_lead_ids = []
            portal_no_response_lead_ids = []
            live_deal_lead_ids = []
            portal_deal_lead_ids = []


            user_id = user.get('user_id') and user['user_id'][0] or False
            user_name = user.get('user_id') and user['user_id'][1] or 'Undefined'

            # 🔹 Step 2: Ab har user ke andar stage-wise grouping karni hai
            stage_data = request.env['crm.lead'].read_group(
                domain=[('type', '=', 'lead'), ('user_id', '=', user_id),('company_id','=',self.env.company.id)],
                fields=['lead_stage_id'],
                groupby=['lead_stage_id']
            )

            user_lead_data = []
            for stage in stage_data:
                stage_id = stage.get('lead_stage_id') and stage['lead_stage_id'][0] or False
                stage_name = stage.get('lead_stage_id') and stage['lead_stage_id'][1] or 'Undefined'

                lead_domain = [('type', '=', 'lead'), ('user_id', '=', user_id)]
                if stage_id:
                    lead_domain.append(('lead_stage_id', '=', stage_id))
                
                total_lead_count = request.env['crm.lead'].search_count(lead_domain)
                lead = request.env['crm.lead'].search(lead_domain, limit=None)

                # Filter leads into live and portal
                live_leads = lead.filtered(lambda lead: lead.live_transfer)
                portal_leads = lead.filtered(lambda lead: not lead.live_transfer)

                live_leads_count = len(live_leads)
                portal_leads_count = len(portal_leads)
                combined_leads = live_leads + portal_leads

                # Calculate duplicates in live and portal leads
                duplicate_stage_ids = request.env['crm.lead.stage'].search([('is_duplicate_stage', '=', True)]).ids
                live_duplicates = live_leads.filtered(lambda lead: lead.lead_stage_id.id in duplicate_stage_ids)
                portal_duplicates = portal_leads.filtered(lambda lead: lead.lead_stage_id.id in duplicate_stage_ids)

                live_duplicates_count = len(live_duplicates)
                portal_duplicates_count = len(portal_duplicates)


                # Calculate dnmc in live and portal leads
                live_dnmc_lead = live_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.object_reason_id.id == 3)
                portal_dnmc_lead = portal_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.object_reason_id.id == 3)

                live_dnmc_lead_count = len(live_dnmc_lead)
                portal_dnmc_lead_count = len(portal_dnmc_lead)

                #calculate live workable and portal workable

                live_workable_lead = live_leads -(live_duplicates + live_dnmc_lead)
                live_workable = live_leads_count -(live_duplicates_count + live_dnmc_lead_count)
                portal_workable = portal_leads_count -(portal_duplicates_count + portal_dnmc_lead_count)
                portal_workable_lead = portal_leads -(portal_duplicates + portal_dnmc_lead)
                
                #total workable
                total_workable_lead = live_workable_lead + portal_workable_lead
                total_workable =  live_workable + portal_workable
                
                #total live and portal declined offer

                live_declined_lead = live_leads.filtered(
                lambda lead: lead.lead_stage_id.id == 5 and lead.dead_reason_id and lead.dead_reason_id.id == 1
                )
                portal_declined_lead = portal_leads.filtered(
                    lambda lead: lead.lead_stage_id.id == 5 and lead.dead_reason_id and lead.dead_reason_id.id == 1
                )

                live_declined_lead_count = len(live_declined_lead)
                portal_declined_lead_count = len(portal_declined_lead)
                
                #live and portal dnc Leads
                dnc_stage_ids = request.env['crm.lead.stage'].search([('is_dnc_stage', '=', True)]).ids
                live_dnc_lead = live_leads.filtered(lambda lead: lead.lead_stage_id.id in dnc_stage_ids)
                portal_dnc_lead = portal_leads.filtered(lambda lead: lead.lead_stage_id.id in dnc_stage_ids)

                live_dnc_lead_count = len(live_dnc_lead)
                portal_dnc_lead_count = len(portal_dnc_lead)

                # live and portal transferred out leads
                live_transferred_lead = live_leads.filtered(lambda lead: lead.lead_stage_id.id == 10)    
                portal_transferred_lead = portal_leads.filtered(lambda lead: lead.lead_stage_id.id == 10)    

                live_transferred_lead_count = len(live_transferred_lead)
                portal_transferred_lead_count = len(portal_transferred_lead)

                #live and portal no contact leads
                live_no_contact_lead = live_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 3)
                portal_no_contact_lead = portal_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 3)

                live_no_contact_lead_count = len(live_no_contact_lead)
                portal_no_contact_lead_count = len(portal_no_contact_lead)    
                
                #live and portal no reponse leads

                live_no_response_lead = live_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 2)
                portal_no_response_lead = portal_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 2)

                live_no_response_lead_count = len(live_no_response_lead)
                portal_no_response_lead_count = len(portal_no_response_lead)
                
                #live and portal leads Converted (Deals)
                live_deal_lead = live_leads.filtered(lambda lead:lead.converted_lead == True and lead.lead_stage_id.id not in [5,7,9])
                portal_deal_lead = portal_leads.filtered(lambda lead:lead.converted_lead == True and lead.lead_stage_id.id not in [5,7,9])

                live_deal_lead_count = len(live_deal_lead)
                portal_deal_lead_count = len(portal_deal_lead)

                #Prime and Subprime lead 
                subprime_lead = lead.filtered(lambda lead:lead.loan_type == 'sub_prime')
                prime_lead = lead.filtered(lambda lead:lead.loan_type != 'sub_prime')
                
                subprime_lead_count = len(subprime_lead)
                prime_lead_count = len(prime_lead)
                
                #Prime and Subprime duplicates lead
                subprime_dup_lead = lead.filtered(lambda lead:lead.loan_type == 'sub_prime' and lead.lead_stage_id.id in duplicate_stage_ids)
                prime_dup_lead = lead.filtered(lambda lead:lead.loan_type != 'sub_prime' and lead.lead_stage_id.id in duplicate_stage_ids)
                
                subprime_dup_lead_count = len(subprime_dup_lead)
                prime_dup_lead_count = len(prime_dup_lead)
                
                #Prime and Subprime dnmc lead
                subprime_dnmc_lead = lead.filtered(lambda lead:lead.loan_type == 'sub_prime' and lead.object_reason_id.id == 3)
                prime_dnmc_lead = lead.filtered(lambda lead:lead.loan_type != 'sub_prime' and lead.object_reason_id.id == 3)
                
                subprime_dnmc_lead_count = len(subprime_dnmc_lead)
                prime_dnmc_lead_count = len(prime_dnmc_lead)
                
                #Prime and Subprime Workable lead

                subprime_workable_lead_ids = []

                for i in subprime_lead:
                    subprime_workable_lead_ids.append(i.id)
                for j in subprime_dup_lead:
                    if j.id in subprime_workable_lead_ids:
                        subprime_workable_lead_ids.remove(j.id)
                for k in subprime_dnmc_lead:
                    if k.id in subprime_workable_lead_ids:
                        subprime_workable_lead_ids.remove(k.id)
                
                
                prime_workable_lead_ids = []

                for i in prime_lead:
                    prime_workable_lead_ids.append(i.id)
                for j in prime_dup_lead:
                    if j.id in prime_workable_lead_ids:
                        prime_workable_lead_ids.remove(j.id)
                for k in prime_dnmc_lead:
                    if k.id in prime_workable_lead_ids:
                        prime_workable_lead_ids.remove(k.id)
                
                subprime_workable_leads = self.env['crm.lead'].search([('id','in',subprime_workable_lead_ids)])
                prime_workable_leads = self.env['crm.lead'].search([('id','in',prime_workable_lead_ids)])

                prime_workable_leads_count = len(prime_workable_lead_ids)
                subprime_workable_leads_count = len(subprime_workable_lead_ids)

                #Prime and Subprime Declined lead
                prime_declined_lead = prime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 1)
                subprime_declined_lead = subprime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 1)
                
                prime_declined_lead_count = len(prime_declined_lead)
                subprime_declined_lead_count = len(subprime_declined_lead)

                #Prime and Subprime Dnc lead
                prime_dnc_lead = prime_workable_leads.filtered(lambda lead: lead.lead_stage_id.id in dnc_stage_ids)
                subprime_dnc_lead = subprime_workable_leads.filtered(lambda lead: lead.lead_stage_id.id in dnc_stage_ids)

                prime_dnc_lead_count = len(prime_dnc_lead)
                subprime_dnc_lead_count = len(subprime_dnc_lead)

                # Prime and Subprime transferred out leads
                prime_transferred_lead = prime_workable_leads.filtered(lambda lead: lead.lead_stage_id.id == 10)    
                subprime_transferred_lead = subprime_workable_leads.filtered(lambda lead: lead.lead_stage_id.id == 10)    

                prime_transferred_lead_count = len(prime_transferred_lead)
                subprime_transferred_lead_count = len(subprime_transferred_lead)

                #live and portal no contact leads
                prime_no_contact_lead = prime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 3)
                subprime_no_contact_lead = subprime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 3)

                prime_no_contact_lead_count = len(prime_no_contact_lead)
                subprime_no_contact_lead_count = len(subprime_no_contact_lead)    
                
                #live and portal no reponse leads

                prime_no_response_lead = prime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 2)
                subprime_no_response_lead = subprime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 2)

                prime_no_response_lead_count = len(prime_no_response_lead)
                subprime_no_response_lead_count = len(subprime_no_response_lead)

                # Update totals
                total_live_leads_count += live_leads_count
                live_leads_ids.extend(live_leads.ids)
                portal_leads_ids.extend(portal_leads.ids)
                combined_leads_ids.extend(combined_leads.ids)
                total_portal_leads_count += portal_leads_count
                total_live_duplicates_count += live_duplicates_count
                live_duplicates_ids.extend(live_duplicates.ids) 
                portal_duplicates_ids.extend(portal_duplicates.ids) 
                total_portal_duplicates_count += portal_duplicates_count
                total_live_dnmc_lead_count += live_dnmc_lead_count 
                live_dnmc_lead_ids.extend(live_dnmc_lead.ids) 
                portal_dnmc_lead_ids.extend(portal_dnmc_lead.ids) 
                total_portal_dnmc_lead_count += portal_dnmc_lead_count 
                total_live_workable_count += live_workable
                live_workable_ids.extend(live_workable_lead.ids) 
                portal_workable_ids.extend(portal_workable_lead.ids) 
                total_portal_workable_count += portal_workable
                total_workable_count += total_workable
                total_workable_ids.extend(total_workable_lead.ids) 
                total_live_declined_lead_count += live_declined_lead_count
                live_declined_lead_ids.extend(live_declined_lead.ids)
                portal_declined_lead_ids.extend(portal_declined_lead.ids)
                total_portal_declined_lead_count += portal_declined_lead_count
                total_live_dnc_lead_count += live_dnc_lead_count
                live_dnc_lead_ids.extend(live_dnc_lead.ids)
                portal_dnc_lead_ids.extend(portal_dnc_lead.ids)
                total_portal_dnc_lead_count += portal_dnc_lead_count
                total_live_transferred_lead_count += live_transferred_lead_count
                live_transferred_lead_ids.extend(live_transferred_lead.ids)
                portal_transferred_lead_ids.extend(portal_transferred_lead.ids)
                total_portal_transferred_lead_count += portal_transferred_lead_count
                total_live_no_contact_lead_count += live_no_contact_lead_count
                live_no_contact_lead_ids.extend(live_no_contact_lead.ids)
                portal_no_contact_lead_ids.extend(portal_no_contact_lead.ids)
                total_portal_no_contact_lead_count += portal_no_contact_lead_count
                total_live_no_response_lead_count += live_no_response_lead_count
                live_no_response_lead_ids.extend(live_no_response_lead.ids)
                portal_no_response_lead_ids.extend(portal_no_response_lead.ids)
                total_portal_no_response_lead_count += portal_no_response_lead_count
                total_live_deal_lead_count += live_deal_lead_count
                live_deal_lead_ids.extend(live_deal_lead.ids)
                portal_deal_lead_ids.extend(portal_deal_lead.ids)
                total_portal_deal_lead_count += portal_deal_lead_count
                total_subprime_lead_count += subprime_lead_count
                total_prime_lead_count += prime_lead_count
                total_subprime_dup_lead_count += subprime_dup_lead_count
                total_prime_dup_lead_count += prime_dup_lead_count
                total_subprime_dnmc_lead_count += subprime_dnmc_lead_count
                total_prime_dnmc_lead_count += prime_dnmc_lead_count
                total_prime_workable_lead_count += prime_workable_leads_count
                total_subprime_workable_lead_count += subprime_workable_leads_count
                total_prime_declined_lead_count += prime_declined_lead_count
                total_subprime_declined_lead_count += subprime_declined_lead_count
                total_prime_dnc_lead_count += prime_dnc_lead_count
                total_subprime_dnc_lead_count += subprime_dnc_lead_count
                total_prime_transferred_lead_count += prime_transferred_lead_count
                total_subprime_transferred_lead_count += subprime_transferred_lead_count
                total_prime_no_contact_lead_count += prime_no_contact_lead_count
                total_subprime_no_contact_lead_count += subprime_no_contact_lead_count
                total_prime_no_response_lead_count += prime_no_response_lead_count
                total_subprime_no_response_lead_count += subprime_no_response_lead_count

                user_lead_data.append({
                    'lead_stage_id': stage_id or 'No Stage',
                    'lead_stage_name': stage_name,  
                    'data': lead.ids,
                })
        
            result.append({
                'user_id': user_id or 'No User Assigned',
                'user_name': user_name,
                'stages': user_lead_data,
                'total_live_lead': total_live_leads_count,
                'live_leads_ids': live_leads_ids,
                'total_portal_lead': total_portal_leads_count,
                'portal_leads_ids': portal_leads_ids,
                'combined_leads_ids': combined_leads_ids,
                'total_live_duplicate': total_live_duplicates_count,  # Total live duplicates
                'live_duplicates_ids': live_duplicates_ids,  # Total live duplicates
                'total_portal_duplicate': total_portal_duplicates_count,  # Total portal duplicates
                'portal_duplicates_ids': portal_duplicates_ids,  # Total portal duplicates
                'total_live_dnmc_lead' : total_live_dnmc_lead_count,
                'live_dnmc_lead_ids': live_dnmc_lead_ids,
                'total_portal_dnmc_lead' : total_portal_dnmc_lead_count,
                'portal_dnmc_lead_ids': portal_dnmc_lead_ids,
                'total_live_workable' : total_live_workable_count,
                'live_workable_ids' : live_workable_ids,
                'portal_workable_ids' : portal_workable_ids,
                'total_portal_workable' : total_portal_workable_count,
                'total_workable_lead' : total_workable_count,
                'total_workable_ids' : total_workable_ids,
                'total_live_declined_lead': total_live_declined_lead_count,
                'live_declined_lead_ids' : live_declined_lead_ids,
                'portal_declined_lead_ids' : portal_declined_lead_ids,
                'total_portal_declined_lead': total_portal_declined_lead_count,
                'total_live_dnc_lead': total_live_dnc_lead_count,
                'live_dnc_lead_ids': live_dnc_lead_ids,
                'portal_dnc_lead_ids': portal_dnc_lead_ids,
                'total_portal_dnc_lead': total_portal_dnc_lead_count,
                'total_live_transferred_lead': total_live_transferred_lead_count,
                'live_transferred_lead_ids': live_transferred_lead_ids,
                'portal_transferred_lead_ids': portal_transferred_lead_ids,
                'total_portal_transferred_lead': total_portal_transferred_lead_count,
                'total_live_no_contact_lead': total_live_no_contact_lead_count,
                'live_no_contact_lead_ids': live_no_contact_lead_ids,
                'portal_no_contact_lead_ids': portal_no_contact_lead_ids,
                'total_portal_no_contact_lead': total_portal_no_contact_lead_count,
                'total_live_no_response_lead': total_live_no_response_lead_count,
                'live_no_response_lead_ids': live_no_response_lead_ids,
                'portal_no_response_lead_ids': portal_no_response_lead_ids,
                'total_portal_no_response_lead': total_portal_no_response_lead_count,
                'total_live_deal_lead': total_live_deal_lead_count,
                'live_deal_lead_ids': live_deal_lead_ids,
                'portal_deal_lead_ids': portal_deal_lead_ids,
                'total_portal_deal_lead': total_portal_deal_lead_count,
                'total_prime_lead' : total_prime_lead_count,
                'total_subprime_lead' : total_subprime_lead_count,
                'total_prime_dup_lead' : total_prime_dup_lead_count,
                'total_subprime_dup_lead' : total_subprime_dup_lead_count,
                'total_prime_dnmc_lead' : total_prime_dnmc_lead_count,
                'total_subprime_dnmc_lead' : total_subprime_dnmc_lead_count,
                'total_subprime_workable_lead' : total_subprime_workable_lead_count,
                'total_prime_workable_lead' : total_prime_workable_lead_count,
                'total_subprime_declined_lead' : total_subprime_declined_lead_count,
                'total_prime_declined_lead' : total_prime_declined_lead_count,
                'total_subprime_dnc_lead' : total_subprime_dnc_lead_count,
                'total_prime_dnc_lead' : total_prime_dnc_lead_count,
                'total_subprime_transferred_lead' : total_subprime_transferred_lead_count,
                'total_prime_transferred_lead' : total_prime_transferred_lead_count,
                'total_subprime_no_contact_lead' : total_subprime_no_contact_lead_count,
                'total_prime_no_contact_lead' : total_prime_no_contact_lead_count,
                'total_subprime_no_response_lead' : total_subprime_no_response_lead_count,
                'total_prime_no_response_lead' : total_prime_no_response_lead_count,
            })

        return result
                                # (2nd Dashboard) Owner Dashboard Ending
                    
                        
                    
                        # (3nd Dashboard) Affiliate Dashboard Starting

    def get_total_crm_lead(self):


        user_data = request.env['crm.lead'].read_group(
            domain=[('type', '=', 'lead')],
            fields=['affiliate_name'],
            groupby=['affiliate_name']
        )

        result = []

        for user in user_data:
            total_live_leads_count = 0
            total_portal_leads_count = 0
            total_live_duplicates_count = 0  # Count for duplicates in live leads
            total_portal_duplicates_count = 0  # Count for duplicates in portal leads
            total_live_dnmc_lead_count = 0
            total_portal_dnmc_lead_count = 0
            total_live_workable_count = 0
            total_portal_workable_count = 0 
            total_workable_count = 0
            total_live_declined_lead_count = 0
            total_portal_declined_lead_count = 0
            total_live_dnc_lead_count = 0
            total_portal_dnc_lead_count = 0
            total_live_transferred_lead_count = 0 
            total_portal_transferred_lead_count = 0 
            total_live_no_contact_lead_count = 0
            total_portal_no_contact_lead_count = 0
            total_live_no_response_lead_count = 0 
            total_portal_no_response_lead_count = 0
            total_live_deal_lead_count = 0
            total_portal_deal_lead_count = 0
            total_subprime_lead_count = 0
            total_prime_lead_count = 0 
            total_subprime_dup_lead_count = 0
            total_prime_dup_lead_count = 0 
            total_subprime_dnmc_lead_count = 0
            total_prime_dnmc_lead_count = 0 
            total_subprime_workable_lead_count = 0
            total_prime_workable_lead_count = 0 
            total_subprime_declined_lead_count = 0
            total_prime_declined_lead_count = 0 
            total_subprime_dnc_lead_count = 0
            total_prime_dnc_lead_count = 0 
            total_prime_transferred_lead_count = 0
            total_subprime_transferred_lead_count = 0
            total_prime_no_contact_lead_count = 0
            total_subprime_no_contact_lead_count = 0
            total_prime_no_response_lead_count = 0
            total_subprime_no_response_lead_count = 0


            live_leads_ids = []
            portal_leads_ids = []
            combined_leads_ids = []
            live_duplicates_ids = []
            portal_duplicates_ids = []
            live_dnmc_lead_ids = []
            portal_dnmc_lead_ids = []
            live_workable_ids = []
            portal_workable_ids = []
            total_workable_ids = []
            live_declined_lead_ids = []
            portal_declined_lead_ids = []
            live_dnc_lead_ids = []
            portal_dnc_lead_ids = []
            live_transferred_lead_ids = []
            portal_transferred_lead_ids = []
            live_no_contact_lead_ids = []
            portal_no_contact_lead_ids = []
            live_no_response_lead_ids = []
            portal_no_response_lead_ids = []
            live_deal_lead_ids = []
            portal_deal_lead_ids = []


            user_id = user.get('affiliate_name') and user['affiliate_name'][0] or False
            user_name = user.get('affiliate_name') and user['affiliate_name'][1] or 'Undefined'

            # 🔹 Step 2: Ab har user ke andar stage-wise grouping karni hai
            stage_data = request.env['crm.lead'].read_group(
                domain=[('type', '=', 'lead'), ('affiliate_name', '=', user_id)],
                fields=['lead_stage_id'],
                groupby=['lead_stage_id']
            )

            user_lead_data = []
            for stage in stage_data:
                stage_id = stage.get('lead_stage_id') and stage['lead_stage_id'][0] or False
                stage_name = stage.get('lead_stage_id') and stage['lead_stage_id'][1] or 'Undefined'

                lead_domain = [('type', '=', 'lead'), ('affiliate_name', '=', user_id)]
                if stage_id:
                    lead_domain.append(('lead_stage_id', '=', stage_id))
                
                total_lead_count = request.env['crm.lead'].search_count(lead_domain)
                lead = request.env['crm.lead'].search(lead_domain, limit=None)

                # Filter leads into live and portal
                live_leads = lead.filtered(lambda lead: lead.live_transfer)
                portal_leads = lead.filtered(lambda lead: not lead.live_transfer)

                live_leads_count = len(live_leads)
                portal_leads_count = len(portal_leads)
                combined_leads = live_leads + portal_leads

                # Calculate duplicates in live and portal leads
                duplicate_stage_ids = request.env['crm.lead.stage'].search([('is_duplicate_stage', '=', True)]).ids
                live_duplicates = live_leads.filtered(lambda lead: lead.lead_stage_id.id in duplicate_stage_ids)
                portal_duplicates = portal_leads.filtered(lambda lead: lead.lead_stage_id.id in duplicate_stage_ids)

                live_duplicates_count = len(live_duplicates)
                portal_duplicates_count = len(portal_duplicates)


                # Calculate dnmc in live and portal leads
                live_dnmc_lead = live_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.object_reason_id.id == 3)
                portal_dnmc_lead = portal_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.object_reason_id.id == 3)

                live_dnmc_lead_count = len(live_dnmc_lead)
                portal_dnmc_lead_count = len(portal_dnmc_lead)

                #calculate live workable and portal workable

                live_workable_lead = live_leads -(live_duplicates + live_dnmc_lead)
                live_workable = live_leads_count -(live_duplicates_count + live_dnmc_lead_count)
                portal_workable = portal_leads_count -(portal_duplicates_count + portal_dnmc_lead_count)
                portal_workable_lead = portal_leads -(portal_duplicates + portal_dnmc_lead)
                
                #total workable
                total_workable_lead =  live_workable_lead + portal_workable_lead
                total_workable =  live_workable + portal_workable
                
                #total live and portal declined offer

                live_declined_lead = live_leads.filtered(
                lambda lead: lead.lead_stage_id.id == 5 and lead.dead_reason_id and lead.dead_reason_id.id == 1
                )
                portal_declined_lead = portal_leads.filtered(
                    lambda lead: lead.lead_stage_id.id == 5 and lead.dead_reason_id and lead.dead_reason_id.id == 1
                )

                live_declined_lead_count = len(live_declined_lead)
                portal_declined_lead_count = len(portal_declined_lead)
                
                #live and portal dnc Leads
                dnc_stage_ids = request.env['crm.lead.stage'].search([('is_dnc_stage', '=', True)]).ids
                live_dnc_lead = live_leads.filtered(lambda lead: lead.lead_stage_id.id in dnc_stage_ids)
                portal_dnc_lead = portal_leads.filtered(lambda lead: lead.lead_stage_id.id in dnc_stage_ids)

                live_dnc_lead_count = len(live_dnc_lead)
                portal_dnc_lead_count = len(portal_dnc_lead)

                # live and portal transferred out leads
                live_transferred_lead = live_leads.filtered(lambda lead: lead.lead_stage_id.id == 10)    
                portal_transferred_lead = portal_leads.filtered(lambda lead: lead.lead_stage_id.id == 10)    

                live_transferred_lead_count = len(live_transferred_lead)
                portal_transferred_lead_count = len(portal_transferred_lead)

                #live and portal no contact leads
                live_no_contact_lead = live_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 3)
                portal_no_contact_lead = portal_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 3)

                live_no_contact_lead_count = len(live_no_contact_lead)
                portal_no_contact_lead_count = len(portal_no_contact_lead)    
                
                #live and portal no reponse leads

                live_no_response_lead = live_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 2)
                portal_no_response_lead = portal_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 2)

                live_no_response_lead_count = len(live_no_response_lead)
                portal_no_response_lead_count = len(portal_no_response_lead)
                
                #live and portal leads Converted (Deals)
                live_deal_lead = live_leads.filtered(lambda lead:lead.converted_lead == True and lead.lead_stage_id.id not in [5,7,9])
                portal_deal_lead = portal_leads.filtered(lambda lead:lead.converted_lead == True and lead.lead_stage_id.id not in [5,7,9])

                live_deal_lead_count = len(live_deal_lead)
                portal_deal_lead_count = len(portal_deal_lead)

                #Prime and Subprime lead
                subprime_lead = lead.filtered(lambda lead:lead.loan_type == 'sub_prime')
                prime_lead = lead.filtered(lambda lead:lead.loan_type != 'sub_prime')
                
                subprime_lead_count = len(subprime_lead)
                prime_lead_count = len(prime_lead)
                
                #Prime and Subprime duplicates lead
                subprime_dup_lead = lead.filtered(lambda lead:lead.loan_type == 'sub_prime' and lead.lead_stage_id.id in duplicate_stage_ids)
                prime_dup_lead = lead.filtered(lambda lead:lead.loan_type != 'sub_prime' and lead.lead_stage_id.id in duplicate_stage_ids)
                
                subprime_dup_lead_count = len(subprime_dup_lead)
                prime_dup_lead_count = len(prime_dup_lead)
                
                #Prime and Subprime dnmc lead
                subprime_dnmc_lead = lead.filtered(lambda lead:lead.loan_type == 'sub_prime' and lead.object_reason_id.id == 3)
                prime_dnmc_lead = lead.filtered(lambda lead:lead.loan_type != 'sub_prime' and lead.object_reason_id.id == 3)
                
                subprime_dnmc_lead_count = len(subprime_dnmc_lead)
                prime_dnmc_lead_count = len(prime_dnmc_lead)
                
                #Prime and Subprime Workable lead

                subprime_workable_lead_ids = []

                for i in subprime_lead:
                    subprime_workable_lead_ids.append(i.id)
                for j in subprime_dup_lead:
                    if j.id in subprime_workable_lead_ids:
                        subprime_workable_lead_ids.remove(j.id)
                for k in subprime_dnmc_lead:
                    if k.id in subprime_workable_lead_ids:
                        subprime_workable_lead_ids.remove(k.id)
                
                
                prime_workable_lead_ids = []

                for i in prime_lead:
                    prime_workable_lead_ids.append(i.id)
                for j in prime_dup_lead:
                    if j.id in prime_workable_lead_ids:
                        prime_workable_lead_ids.remove(j.id)
                for k in prime_dnmc_lead:
                    if k.id in prime_workable_lead_ids:
                        prime_workable_lead_ids.remove(k.id)
                
                subprime_workable_leads = self.env['crm.lead'].search([('id','in',subprime_workable_lead_ids)])
                prime_workable_leads = self.env['crm.lead'].search([('id','in',prime_workable_lead_ids)])

                prime_workable_leads_count = len(prime_workable_lead_ids)
                subprime_workable_leads_count = len(subprime_workable_lead_ids)

                #Prime and Subprime Declined lead
                prime_declined_lead = prime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 1)
                subprime_declined_lead = subprime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 1)
                
                prime_declined_lead_count = len(prime_declined_lead)
                subprime_declined_lead_count = len(subprime_declined_lead)

                #Prime and Subprime Dnc lead
                prime_dnc_lead = prime_workable_leads.filtered(lambda lead: lead.lead_stage_id.id in dnc_stage_ids)
                subprime_dnc_lead = subprime_workable_leads.filtered(lambda lead: lead.lead_stage_id.id in dnc_stage_ids)

                prime_dnc_lead_count = len(prime_dnc_lead)
                subprime_dnc_lead_count = len(subprime_dnc_lead)

                # Prime and Subprime transferred out leads
                prime_transferred_lead = prime_workable_leads.filtered(lambda lead: lead.lead_stage_id.id == 10)    
                subprime_transferred_lead = subprime_workable_leads.filtered(lambda lead: lead.lead_stage_id.id == 10)    

                prime_transferred_lead_count = len(prime_transferred_lead)
                subprime_transferred_lead_count = len(subprime_transferred_lead)

                #live and portal no contact leads
                prime_no_contact_lead = prime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 3)
                subprime_no_contact_lead = subprime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 3)

                prime_no_contact_lead_count = len(prime_no_contact_lead)
                subprime_no_contact_lead_count = len(subprime_no_contact_lead)    
                
                #live and portal no reponse leads

                prime_no_response_lead = prime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 2)
                subprime_no_response_lead = subprime_workable_leads.filtered(lambda lead:lead.lead_stage_id.id == 5 and lead.dead_reason_id.id == 2)

                prime_no_response_lead_count = len(prime_no_response_lead)
                subprime_no_response_lead_count = len(subprime_no_response_lead)

                # Update totals
                total_live_leads_count += live_leads_count
                live_leads_ids.extend(live_leads.ids)
                portal_leads_ids.extend(portal_leads.ids)
                combined_leads_ids.extend(combined_leads.ids)
                total_portal_leads_count += portal_leads_count
                total_live_duplicates_count += live_duplicates_count
                live_duplicates_ids.extend(live_duplicates.ids) 
                portal_duplicates_ids.extend(portal_duplicates.ids)
                total_portal_duplicates_count += portal_duplicates_count
                total_live_dnmc_lead_count += live_dnmc_lead_count 
                live_dnmc_lead_ids.extend(live_dnmc_lead.ids) 
                portal_dnmc_lead_ids.extend(portal_dnmc_lead.ids)
                total_portal_dnmc_lead_count += portal_dnmc_lead_count 
                total_live_workable_count += live_workable
                live_workable_ids.extend(live_workable_lead.ids)
                portal_workable_ids.extend(portal_workable_lead.ids)
                total_portal_workable_count += portal_workable
                total_workable_count += total_workable
                total_workable_ids.extend(total_workable_lead.ids)
                total_live_declined_lead_count += live_declined_lead_count
                live_declined_lead_ids.extend(live_declined_lead.ids)
                portal_declined_lead_ids.extend(portal_declined_lead.ids)
                total_portal_declined_lead_count += portal_declined_lead_count
                total_live_dnc_lead_count += live_dnc_lead_count
                live_dnc_lead_ids.extend(live_dnc_lead.ids)
                portal_dnc_lead_ids.extend(portal_dnc_lead.ids)
                total_portal_dnc_lead_count += portal_dnc_lead_count
                total_live_transferred_lead_count += live_transferred_lead_count
                live_transferred_lead_ids.extend(live_transferred_lead.ids)
                portal_transferred_lead_ids.extend(portal_transferred_lead.ids)
                total_portal_transferred_lead_count += portal_transferred_lead_count
                total_live_no_contact_lead_count += live_no_contact_lead_count
                live_no_contact_lead_ids.extend(live_no_contact_lead.ids)
                portal_no_contact_lead_ids.extend(portal_no_contact_lead.ids)
                total_portal_no_contact_lead_count += portal_no_contact_lead_count
                total_live_no_response_lead_count += live_no_response_lead_count
                live_no_response_lead_ids.extend(live_no_response_lead.ids)
                portal_no_response_lead_ids.extend(portal_no_response_lead.ids)
                total_portal_no_response_lead_count += portal_no_response_lead_count
                total_live_deal_lead_count += live_deal_lead_count
                live_deal_lead_ids.extend(live_deal_lead.ids)
                portal_deal_lead_ids.extend(portal_deal_lead.ids)
                total_portal_deal_lead_count += portal_deal_lead_count
                total_subprime_lead_count += subprime_lead_count
                total_prime_lead_count += prime_lead_count
                total_subprime_dup_lead_count += subprime_dup_lead_count
                total_prime_dup_lead_count += prime_dup_lead_count
                total_subprime_dnmc_lead_count += subprime_dnmc_lead_count
                total_prime_dnmc_lead_count += prime_dnmc_lead_count
                total_prime_workable_lead_count += prime_workable_leads_count
                total_subprime_workable_lead_count += subprime_workable_leads_count
                total_prime_declined_lead_count += prime_declined_lead_count
                total_subprime_declined_lead_count += subprime_declined_lead_count
                total_prime_dnc_lead_count += prime_dnc_lead_count
                total_subprime_dnc_lead_count += subprime_dnc_lead_count
                total_prime_transferred_lead_count += prime_transferred_lead_count
                total_subprime_transferred_lead_count += subprime_transferred_lead_count
                total_prime_no_contact_lead_count += prime_no_contact_lead_count
                total_subprime_no_contact_lead_count += subprime_no_contact_lead_count
                total_prime_no_response_lead_count += prime_no_response_lead_count
                total_subprime_no_response_lead_count += subprime_no_response_lead_count

                user_lead_data.append({
                    'lead_stage_id': stage_id or 'No Stage',
                    'lead_stage_name': stage_name,  
                    'data': lead.ids,
                })

            result.append({
                'user_id': user_id or 'No User Assigned',
                'user_name': user_name,
                'stages': user_lead_data,
                'total_live_lead': total_live_leads_count,
                'live_leads_ids' : live_leads_ids,
                'portal_leads_ids' : portal_leads_ids,
                'combined_leads_ids' : combined_leads_ids,
                'total_portal_lead': total_portal_leads_count,
                'total_live_duplicate': total_live_duplicates_count,  # Total live duplicates
                'live_duplicates_ids' : live_duplicates_ids,
                'portal_duplicates_ids' : portal_duplicates_ids,
                'total_portal_duplicate': total_portal_duplicates_count,  # Total portal duplicates
                'total_live_dnmc_lead' : total_live_dnmc_lead_count,
                'live_dnmc_lead_ids' : live_dnmc_lead_ids, 
                'portal_dnmc_lead_ids' : portal_dnmc_lead_ids,
                'total_portal_dnmc_lead' : total_portal_dnmc_lead_count,
                'total_live_workable' : total_live_workable_count,
                'live_workable_ids' : live_workable_ids,
                'portal_workable_ids' : portal_workable_ids,
                'total_portal_workable' : total_portal_workable_count,
                'total_workable_lead' : total_workable_count,
                'total_workable_ids' : total_workable_ids,
                'total_live_declined_lead': total_live_declined_lead_count,
                'live_declined_lead_ids' : live_declined_lead_ids,
                'portal_declined_lead_ids' : portal_declined_lead_ids,
                'total_portal_declined_lead': total_portal_declined_lead_count,
                'total_live_dnc_lead': total_live_dnc_lead_count,
                'live_dnc_lead_ids' : live_dnc_lead_ids,
                'portal_dnc_lead_ids' : portal_dnc_lead_ids,
                'total_portal_dnc_lead': total_portal_dnc_lead_count,
                'total_live_transferred_lead': total_live_transferred_lead_count,
                'live_transferred_lead_ids' : live_transferred_lead_ids,
                'portal_transferred_lead_ids' : portal_transferred_lead_ids,
                'total_portal_transferred_lead': total_portal_transferred_lead_count,
                'total_live_no_contact_lead': total_live_no_contact_lead_count,
                'live_no_contact_lead_ids' : live_no_contact_lead_ids,
                'portal_no_contact_lead_ids' : portal_no_contact_lead_ids,
                'total_portal_no_contact_lead': total_portal_no_contact_lead_count,
                'total_live_no_response_lead': total_live_no_response_lead_count,
                'live_no_response_lead_ids' : live_no_response_lead_ids,
                'portal_no_response_lead_ids' : portal_no_response_lead_ids,
                'total_portal_no_response_lead': total_portal_no_response_lead_count,
                'total_live_deal_lead': total_live_deal_lead_count,
                'live_deal_lead_ids' : live_deal_lead_ids,
                'portal_deal_lead_ids' : portal_deal_lead_ids,
                'total_portal_deal_lead': total_portal_deal_lead_count,
                'total_prime_lead' : total_prime_lead_count,
                'total_subprime_lead' : total_subprime_lead_count,
                'total_prime_dup_lead' : total_prime_dup_lead_count,
                'total_subprime_dup_lead' : total_subprime_dup_lead_count,
                'total_prime_dnmc_lead' : total_prime_dnmc_lead_count,
                'total_subprime_dnmc_lead' : total_subprime_dnmc_lead_count,
                'total_subprime_workable_lead' : total_subprime_workable_lead_count,
                'total_prime_workable_lead' : total_prime_workable_lead_count,
                'total_subprime_declined_lead' : total_subprime_declined_lead_count,
                'total_prime_declined_lead' : total_prime_declined_lead_count,
                'total_subprime_dnc_lead' : total_subprime_dnc_lead_count,
                'total_prime_dnc_lead' : total_prime_dnc_lead_count,
                'total_subprime_transferred_lead' : total_subprime_transferred_lead_count,
                'total_prime_transferred_lead' : total_prime_transferred_lead_count,
                'total_subprime_no_contact_lead' : total_subprime_no_contact_lead_count,
                'total_prime_no_contact_lead' : total_prime_no_contact_lead_count,
                'total_subprime_no_response_lead' : total_subprime_no_response_lead_count,
                'total_prime_no_response_lead' : total_prime_no_response_lead_count,
            })

        return result


                                # (3nd Dashboard) Affiliate Dashboard Ending

class CRMCustomDashboardController(http.Controller):

    @http.route('/crm_dashboard/get_open_leads', type='json', auth='user')
    def get_open_leads(self):
        """
        Call the `get_open_leads` function from the `crm.lead` model.
        """
        # Context se date_domain fetch karo agar zaroori ho
        date_domain = get_today_date_domain()  # Tum yaha filter add kar sakte ho
        
        # Model function call karna
        leads_data = request.env['crm.lead'].get_open_leads(date_domain)

        all_ids = []
        for record in leads_data:
            all_ids.extend(record['data'])

        # Response return karna JSON format me
        return {'open_leads': leads_data, 'open_leads_ids':all_ids}
    

    
    @http.route('/crm_dashboard/get_duplicate_stages', type='json', auth='user')
    def get_duplicate_stages(self):

        date_domain = []
        duplicate_leads = request.env['crm.lead'].get_duplicate_stage(date_domain)
        all_ids = []
        for record in duplicate_leads:
            all_ids.extend(record['data'])

        return {'duplicate_leads': duplicate_leads,'duplicate_leads_ids':all_ids}
    


    @http.route('/crm_dashboard/get_dnmc', type='json', auth='user')
    def get_dnmc(self):
        date_domain =  get_today_date_domain()
        
        try: 
            dnmc_leads = request.env['crm.lead'].get_dnmc(date_domain)
            all_ids = []
            for record in dnmc_leads:
                all_ids.extend(record['data'])
            return {'dnmc_leads': dnmc_leads if isinstance(dnmc_leads, list) else [],
                    'dnmc_leads_ids': all_ids
                    }
            
        except Exception as e:
            return [e]
    

    @http.route('/crm_dashboard/get_converted_leads', type='json', auth='user')
    def get_converted_leads(self):
        date_domain =  get_today_date_domain()
        
        try:
            converted_leads = request.env['crm.lead'].get_converted_leads(date_domain)

            # Safely extract all IDs from the list of dicts
            converted_ids = []
            for lead in converted_leads:
                converted_ids.extend(lead['data'])  # or append if 'data' is a single id

            return {
                'converted_leads': converted_leads if isinstance(converted_leads, list) else [],
                'converted_lead_ids': converted_ids
            }

        except Exception as e:
            return {'error': str(e)}

        # try:
        #     converted_leads = request.env['crm.lead'].get_converted_leads(date_domain)
        #     return {'converted_leads': converted_leads if isinstance(converted_leads, list) else [],'converted_lead_ids':converted_leads.data}
        
        # except Exception as e:
        #     return [e]


    @http.route('/crm_dashboard/get_dead_declined', type='json', auth='user')
    def get_dead_declined(self):
        date_domain =  get_today_date_domain()
        
        try:
            dead_leads = request.env['crm.lead'].get_dead_declined(date_domain)
            all_ids = []
            for record in dead_leads:
                all_ids.extend(record['data'])
            return {'dead_leads': dead_leads if isinstance(dead_leads, list) else [],
                    'dead_leads_ids' :all_ids
                    }
            
        except Exception as e:
            return [e]


    @http.route('/crm_dashboard/get_consultation_processing', type='json', auth='user')
    def get_consultation_processing(self):
        """
        Call the `get_consultation_processing` function from the `crm.lead` model.
        """
        # Context se date_domain fetch karo agar zaroori ho
        date_domain = get_today_date_domain()  # Tum yaha filter add kar sakte ho
        
        # Model function call karna
        leads_data = request.env['crm.lead'].get_consultation_processing(date_domain)

        all_ids = []
        for record in leads_data:
            all_ids.extend(record['data'])

        # Response return karna JSON format me
        return {'consultation_processing': leads_data, 'consultation_processing_ids':all_ids}
    
    
    @http.route('/crm_dashboard/get_application_in_process', type='json', auth='user')
    def get_application_in_process(self):
        """
        Call the `get_application_in_process` function from the `crm.lead` model.
        """
        # Context se date_domain fetch karo agar zaroori ho
        date_domain = get_today_date_domain()  # Tum yaha filter add kar sakte ho
        
        # Model function call karna
        leads_data = request.env['crm.lead'].get_application_in_process(date_domain)

        all_ids = []
        for record in leads_data:
            all_ids.extend(record['data'])

        # Response return karna JSON format me
        return {'application_in_process': leads_data, 'application_in_process_ids':all_ids}
    
    
    @http.route('/crm_dashboard/get_freeze_processing', type='json', auth='user')
    def get_freeze_processing(self):
        """
        Call the `get_freeze_processing` function from the `crm.lead` model.
        """
        # Context se date_domain fetch karo agar zaroori ho
        date_domain = get_today_date_domain()  # Tum yaha filter add kar sakte ho
        
        # Model function call karna
        leads_data = request.env['crm.lead'].get_freeze_processing(date_domain)

        all_ids = []
        for record in leads_data:
            all_ids.extend(record['data'])

        # Response return karna JSON format me
        return {'freeze_processing': leads_data, 'freeze_processing_ids':all_ids}
    
    
    @http.route('/crm_dashboard/get_processing', type='json', auth='user')
    def get_processing(self):
        """
        Call the `get_processing` function from the `crm.lead` model.
        """
        # Context se date_domain fetch karo agar zaroori ho
        date_domain = get_today_date_domain()  # Tum yaha filter add kar sakte ho
        
        # Model function call karna
        leads_data = request.env['crm.lead'].get_processing(date_domain)

        all_ids = []
        for record in leads_data:
            all_ids.extend(record['data'])

        # Response return karna JSON format me
        return {'processing': leads_data, 'processing_ids':all_ids}
    
    
    @http.route('/crm_dashboard/get_add_lender', type='json', auth='user')
    def get_add_lender(self):
        """
        Call the `get_add_lender` function from the `crm.lead` model.
        """
        # Context se date_domain fetch karo agar zaroori ho
        date_domain = get_today_date_domain()  # Tum yaha filter add kar sakte ho
        
        # Model function call karna
        leads_data = request.env['crm.lead'].get_add_lender(date_domain)

        all_ids = []
        for record in leads_data:
            all_ids.extend(record['data'])

        # Response return karna JSON format me
        return {'add_lender': leads_data, 'add_lender_ids':all_ids}
    

    @http.route('/crm_dashboard/get_submitting_docs', type='json', auth='user')
    def get_submitting_docs(self):
        """
        Call the `get_submitting_docs` function from the `crm.lead` model.
        """
        # Context se date_domain fetch karo agar zaroori ho
        date_domain = get_today_date_domain()  # Tum yaha filter add kar sakte ho
        
        # Model function call karna
        leads_data = request.env['crm.lead'].get_submitting_docs(date_domain)

        all_ids = []
        for record in leads_data:
            all_ids.extend(record['data'])

        # Response return karna JSON format me
        return {'submitting_docs': leads_data, 'submitting_docs_ids':all_ids}
    

    @http.route('/crm_dashboard/get_signed_closing_docs', type='json', auth='user')
    def get_signed_closing_docs(self):
        """
        Call the `get_signed_closing_docs` function from the `crm.lead` model.
        """
        # Context se date_domain fetch karo agar zaroori ho
        date_domain = get_today_date_domain()  # Tum yaha filter add kar sakte ho
        
        # Model function call karna
        leads_data = request.env['crm.lead'].get_signed_closing_docs(date_domain)

        all_ids = []
        for record in leads_data:
            all_ids.extend(record['data'])

        # Response return karna JSON format me
        return {'signed_closing_docs': leads_data, 'signed_closing_docs_ids':all_ids}
    

    @http.route('/crm_dashboard/get_pending_processing', type='json', auth='user')
    def get_pending_processing(self):
        """
        Call the `get_pending_processing` function from the `crm.lead` model.
        """
        # Context se date_domain fetch karo agar zaroori ho
        date_domain = get_today_date_domain()  # Tum yaha filter add kar sakte ho
        
        # Model function call karna
        leads_data = request.env['crm.lead'].get_pending_processing(date_domain)

        all_ids = []
        for record in leads_data:
            all_ids.extend(record['data'])

        # Response return karna JSON format me
        return {'pending_processing': leads_data, 'pending_processing_ids':all_ids}
    
    

    # for Weekly Sales Dashboard

    @http.route('/crm_dashboard/get_total_leads', type='json', auth='user')
    def get_total_leads(self):
        """
        Call the `get_total_leads` function from the `crm.lead` model.
        """
        # Context se date_domain fetch karo agar zaroori ho
        # date_domain = get_today_date_domain()  # Tum yaha filter add kar sakte ho
        
        # Model function call karna
        # total_leads_data = request.env['crm.lead'].get_total_leads()
        total_leads_data_new = request.env['crm.lead'].get_total_leads_new()

        # Response return karna JSON format me
        # return {'total_leads_data': total_leads_data , 'get_total_leads_new':total_leads_data_new}
        return {'get_total_leads_new':total_leads_data_new}
    


    @http.route('/crm_dashboard/get_total_crm_lead', type='json', auth='user')
    def get_total_crm_lead(self):
        """
        Call the `get_total_leads` function from the `crm.lead` model.
        """
        
        # Model function call karna

        # total_crm_lead_data_fields = request.env['crm.lead'].get_total_crm_leads()
        total_crm_leads_data = request.env['crm.lead'].get_total_crm_lead()

        # Response return karna JSON format me
        return {
            'total_crm_leads_data':total_crm_leads_data,
            # 'total_crm_lead_data_fields':total_crm_lead_data_fields
            }