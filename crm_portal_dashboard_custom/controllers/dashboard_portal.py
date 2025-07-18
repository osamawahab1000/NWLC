# -*- coding: utf-8 -*-
from odoo.addons.portal.controllers import portal as payment_portal
from odoo.addons.portal_crm_custom.controllers import portal as CustomerPortal 
from odoo.http import request
from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import UserError
import ast

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager



class DashboardCustomerPortal(CustomerPortal):



    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'crm_lead_dashboard_count' in counters:
            values['crm_lead_dashboard_count'] = 1

        return values
    
    # def get_open_leads(self):
    #     not_dead_n_dnc_stage = request.env['crm.lead.stage'].search([('is_dnc_stage','=',False),('is_dead_stage','=',False),('is_duplicate_stage','=',False)])
            

    #     # raise UserError(not_dead_n_dnc_stage)
    #     if not_dead_n_dnc_stage:
    #         ids = not_dead_n_dnc_stage.ids 
    #         stage_data = request.env['crm.lead'].read_group(
    #             domain=[('lead_stage_id.id','in', ids),('type','=','lead')],
    #             fields=['lead_stage_id'],  # Field to group by
    #             groupby=['lead_stage_id']  # Grouping field
    #             ) 
    #         result = [
    #             {
    #                 'stage_name': stage['lead_stage_id'][1] if stage['lead_stage_id'] else 'Undefined',
    #                 'count': request.env['crm.lead'].search_count(domain=[('type','=','lead'),('lead_stage_id','in',not_dead_n_dnc_stage.ids)]), #
    #                 'data': request.env['crm.lead'].search(domain=[('type','=','lead'),('lead_stage_id','in',not_dead_n_dnc_stage.ids)]).ids
    #             }
    #             for stage in stage_data
    #         ]
    #         return result
    


    def get_open_leads(self, date_domain):
        # Fetch all valid stages excluding DNC, dead, and duplicate stages
        not_dead_n_dnc_stage = request.env['crm.lead.stage'].search(
            [('is_dnc_stage', '=', False), ('is_dead_stage', '=', False), ('is_duplicate_stage', '=', False)]
        )

        if not not_dead_n_dnc_stage:
            return []

        # Group leads by stage
        stage_data = request.env['crm.lead'].read_group(
            domain=[('lead_stage_id.id', 'in', not_dead_n_dnc_stage.ids), ('type', '=', 'lead')] + date_domain,
            fields=['lead_stage_id'],  # Field to group by
            groupby=['lead_stage_id']  # Grouping field
        )

        # Prepare results with filtering of zero-count stages
        result = []

        for stage in stage_data:
            # Skip stages with no leads
            if stage['lead_stage_id_count'] == 0:
                continue

            # Extract stage details
            stage_id = stage['lead_stage_id'][0] if stage['lead_stage_id'] else None
            stage_name = stage['lead_stage_id'][1] if stage['lead_stage_id'] else 'Undefined'

            # Fetch leads specific to the current stage
            if stage_id:
                leads_domain = [('type', '=', 'lead'), ('lead_stage_id', '=', stage_id)] + date_domain
                lead_count = request.env['crm.lead'].search_count(leads_domain)
                leads = request.env['crm.lead'].search(leads_domain)

                # Append stage-specific data
                result.append({
                    'stage_name': stage_name,
                    'count': lead_count,
                    'data': leads.ids,
                })

        return result

    def get_lead_stage_unworkable_leadS(self,date_domain):
        dead_reson = request.env['dead.reason'].search([('is_unworkable_lead','=',True)])
        dead_stage = request.env['crm.lead.stage'].search([('is_dead_stage','=',True)])
        unworkable_data = request.env['crm.lead'].read_group(
            domain=[('dead_reason_id','in',dead_reson.ids)] + date_domain,  # Add domain if filtering is needed (e.g., specific company or user)
            fields=['dead_reason_id'],  # Field to group by
            groupby=['dead_reason_id']  # Grouping field
            )

        
        
        result = [
            {
                'stage_name': stage['dead_reason_id'][1] if stage['dead_reason_id'] else 'Undefined',
                'count': request.env['crm.lead'].sudo().search_count([('dead_reason_id','=',stage['dead_reason_id'][0]),('type','=','lead')] + date_domain), #
                'data': request.env['crm.lead'].sudo().search([('dead_reason_id','=',stage['dead_reason_id'][0]),('type','=','lead')]+ date_domain).ids, #

            }
            for stage in unworkable_data
        ]
        return result
    def get_duplicate_stage(self,date_domain):
        dup_stage = request.env['crm.lead.stage'].search([('is_duplicate_stage','=',True)])
        # raise UserError(dup_stage.ids)
        dup_data = request.env['crm.lead'].sudo().search_count(
            [('lead_stage_id','in',dup_stage.ids)]+ date_domain,
        )
        
        
        return [{
                'count': dup_data
            }]
    
    def get_lead_stage_dead_leadS(self,date_domain):
        

        dead_reson = request.env['dead.reason'].search([('is_dead_lead','=',True)])
        dead_lead_data = request.env['crm.lead'].read_group(
            domain=[('dead_reason_id','in',dead_reson.ids),('type','=','lead')] + date_domain,  
            fields=['dead_reason_id',],  
            groupby=['dead_reason_id']
        )
        result = [
            {
                'stage_name': stage['dead_reason_id'][1] if stage['dead_reason_id'] else 'Undefined',
                'count': request.env['crm.lead'].sudo().search_count([('dead_reason_id','=',stage['dead_reason_id'][0]),('type','=','lead')] + date_domain,), #
                'data': request.env['crm.lead'].sudo().search([('dead_reason_id','=',stage['dead_reason_id'][0]),('type','=','lead')]+date_domain).ids
            }
            for stage in dead_lead_data
        ]

        dnc_stage = request.env['crm.lead.stage'].search([('is_dnc_stage','=',True)])

        dnc_lead_data = request.env['crm.lead'].read_group(
            domain=[('lead_stage_id','in',dnc_stage.ids)] + date_domain,  
            fields=['lead_stage_id'],  
            groupby=['lead_stage_id']
        )
        for dnc in dnc_lead_data:
            if dnc['lead_stage_id'][0] in dnc_stage.ids:
                result.append(
                    {
                        'stage_name': dnc['lead_stage_id'][1] if dnc['lead_stage_id'] else 'Undefined',
                        'count': request.env['crm.lead'].sudo().search_count([('lead_stage_id','in',dnc_stage.ids),('type','=','lead')] +date_domain),
                        'data':request.env['crm.lead'].sudo().search([('lead_stage_id','in',dnc_stage.ids),('type','=','lead')]+ date_domain).ids #
                    }
                )
        return result


    # Processing 


    def _prepare_crm_lead_portal_dashboard_rendering_values(
        self, page=1, date_begin=None, date_end=None, sortby=None,return_crm_lead_page=False, **kwargs):

        start_date = kwargs.get('start_date')
        start_date_domain = False
        end_date_domain = False
        end_date = kwargs.get('end_date')
        start_date_domain = ('date_created', '>=', start_date) if start_date else []
        end_date_domain = ('date_created', '<=', end_date) if end_date else []
        

        date_domain = []
        if start_date_domain:
            date_domain.append(start_date_domain)
        if end_date_domain:
            date_domain.append(end_date_domain)
        
        leads_open_lead = self.get_open_leads(date_domain)
        lead_unworkable_lead = self.get_lead_stage_unworkable_leadS(date_domain)
        lead_dead_lead = self.get_lead_stage_dead_leadS(date_domain)
        lead_duplicate_lead = self.get_duplicate_stage(date_domain)




       
        totals = {
            "unworkable_total" : sum(unwork['count'] for unwork in lead_unworkable_lead),
            "open_lead_total" : sum(open_lead['count'] for open_lead in leads_open_lead),
            "dead_lead_total" : sum(dead_lead['count'] for dead_lead in lead_dead_lead),
            "duplicate_lead_total" : sum(duplicate_lead['count'] for duplicate_lead in lead_duplicate_lead),
        }
        

        grand_total = sum(totals.values())

        # Calculate percentages for each category relative to the grand total
        percentages = {
            key: round((value / grand_total * 100),2) if grand_total > 0 else 0
            for key, value in totals.items()
        }

       
       
       

        values = {}
        values.update({
            'date': date_begin,
            'dashboard': True,
            'totals':totals,
            'percentages' :percentages,
            'grand_total':grand_total,
            'lead_open_lead':leads_open_lead,
            'lead_unworkable_lead':lead_unworkable_lead,
            'lead_dead_lead':lead_dead_lead,
            'start_date':start_date,
            'end_date':end_date,
            'customers': None,
            'page_name': 'crm_lead_dashboard',
            'pager': None,
            'default_url': '/my/lead/dashboard',
            'searchbar_sortings': None,
            'sortby': None,
            'search_in':'content'
        })
        
        return values
    
    @http.route(['/my/lead/dashboard'], type='http', auth="user", website=True)
    def portal_my_crm_lead_dashboard(self, **kwargs):
        values = self._prepare_crm_lead_portal_dashboard_rendering_values(**kwargs)

        return request.render("crm_portal_dashboard_custom.portal_my_crm_lead_dashboard", values)
    


    def _prepare_crm_lead_portal_rendering_values_dashboard(
        self, page=1, date_begin=None, date_end=None, sortby=None, return_crm_lead_page=False, **kwargs
    ):
        # Call the parent method to get the initial values
        values = super(DashboardCustomerPortal, self)._prepare_crm_lead_portal_rendering_values_dashboard(
            page=page, 
            date_begin=date_begin,
            date_end=date_end, 
            sortby=sortby, 
            return_crm_lead_page=return_crm_lead_page, 
            **kwargs
        )
        lead_data = kwargs.get('leads_data')
        data = request.env['crm.lead'].search([('id','in',ast.literal_eval(lead_data))])
        values.update({
            'leads': data,  # Example: Adding high-priority leads
        })

        return values
    




        
