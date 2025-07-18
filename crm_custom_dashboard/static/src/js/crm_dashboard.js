/** @odoo-module **/
import { registry } from "@web/core/registry";
import { loadJS } from '@web/core/assets';
import { useService } from "@web/core/utils/hooks";
import { useState } from "@odoo/owl"; 
import { WebClient } from "@web/webclient/webclient";
import { _t } from "@web/core/l10n/translation";

const { Component, useRef, mount, onWillStart, onMounted} = owl;
import { rpc } from "@web/core/network/rpc";

export class OdooCRMDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        
        this.state = useState({
        // (1st Dashboard) Daily count dashboard Starting
            open_leads: [],   
            open_leads_ids: false,     
            total_open_leads: 0,
            consultation_processing: [],   
            consultation_processing_ids: false,     
            total_consultation_processing: 0,
            application_in_process: [],   
            application_in_process_ids: false,     
            total_application_in_process: 0,
            freeze_processing: [],   
            freeze_processing_ids: false,     
            total_freeze_processing: 0,
            processing: [],   
            processing_ids: false,     
            total_processing: 0,
            add_lender: [],   
            add_lender_ids: false,     
            total_add_lender: 0,
            submitting_docs: [],   
            submitting_docs_ids: false,     
            total_submitting_docs: 0,
            signed_closing_docs: [],   
            signed_closing_docs_ids: false,     
            total_signed_closing_docs: 0,
            pending_processing: [],   
            pending_processing_ids: false,     
            total_pending_processing: 0,
            duplicate_leads: [],
            duplicate_leads_ids: false,
            total_duplicate_leads: 0,
            dnmc_leads: [],
            dnmc_leads_ids: false,
            total_dnmc_leads: 0,
            converted_leads: [],
            converted_leads_ids: false,
            total_converted_leads: 0,
            dead_leads: [],
            dead_leads_ids: false,
            total_dead_leads: 0,
        // (1st Dashboard) Daily count dashboard Ending

        // (2nd Dashboard) Owner dashboard Start
            total_leads_data: [],
            total_crm_leads: 0,
            total_live_leads: 0,
            total_portal_leads: 0,
            total_live_duplicates: 0,
            total_portal_duplicates: 0,
            total_live_dnmc_leads: 0,
            total_portal_dnmc_leads: 0,
            total_live_workables :0,
            total_portal_workables :0,
            total_workables : 0,
            total_live_declined_leads : 0,
            total_portal_declined_leads :0,
            total_live_dnc_leads : 0,
            total_portal_dnc_leads :0,
            total_live_transferred_leads : 0,
            total_portal_transferred_leads : 0,
            total_live_no_contact_leads : 0,
            total_portal_no_contact_leads : 0,
            total_live_no_response_leads : 0,
            total_portal_no_response_leads : 0,
            total_live_deal_leads : 0,
            total_portal_deal_leads : 0,
            weekly_sales_rep_dashboard: [],
            // (2nd Dashboard) Owner dashboard Ending


            // (3rd Dashboard) Affiliate dashboard Starting
            affiliateweekly_sales_rep_dashboard: []
            // (3rd Dashboard) Affiliate dashboard Ending
        });

        onWillStart( () => {
             this.fetchOpenLeads();
             this.fetchConsultationProcessing();
             this.fetchApplicationInProcess();
             this.fetchFreezeProcessing();
             this.fetchProcessing();
             this.fetchAddLender();
             this.fetchSubmittingDocs();
             this.fetchSignedClosingDocs();
             this.fetchPendingProcessing();
             this.fetchDuplicateLeads();
             this.fetchDnmcLeads();
             this.fetchConvertedLeads();
             this.fetchDeadDeclinedLeads();
             this.fetchTotalLeads();
             this.fetchTotalSalesLeads();
        });
    }
        // ----------------------(1st Dashboard) Daily count dashboard Starting ----------------------

    async fetchOpenLeads() {
        try {
            const result = await rpc('/crm_dashboard/get_open_leads', {});
            if (result && result.open_leads) {
                this.state.open_leads = result.open_leads;
                this.state.total_open_leads = result.open_leads.reduce((sum, stage) => sum + stage.count, 0);
                this.state.open_leads_ids = result.open_leads_ids;
            } 
        } catch (error) {
            console.error("Error fetching open leads:", error);
        }
    }
    
    async fetchDuplicateLeads() {
        try {

            
            const result = await rpc('/crm_dashboard/get_duplicate_stages', {});
            console.log('result',result)
            if (result && result.duplicate_leads) {
                    this.state.duplicate_leads = result.duplicate_leads;
                    this.state.total_duplicate_leads = result.duplicate_leads.reduce((sum, stage) => sum + stage.count, 0);
                    this.state.duplicate_leads_ids = result.duplicate_leads_ids
                }
        } catch (error) {
            console.log("Error fetching duplicate leads:" + String(error));
        }
    }
    
    async fetchDnmcLeads() {
        try {
            const result = await rpc('/crm_dashboard/get_dnmc', {});
            
            console.log("DNMC Leads API Response:", result);
            
            if (result && Array.isArray(result.dnmc_leads)) {  // ✅ Ensure it's an array
                this.state.dnmc_leads = result.dnmc_leads;
                this.state.total_dnmc_leads = result.dnmc_leads.reduce((sum, item) => sum + item.count, 0);
                this.state.dnmc_leads_ids = result.dnmc_leads_ids
            } else {
                console.error("DNMC leads is not an array:", result.dnmc_leads);
            }
        } catch (error) {
            console.error("Error fetching DNMC leads:", error);
        }
    }
    
    
    async fetchConvertedLeads() {
        try {
            const result = await rpc('/crm_dashboard/get_converted_leads', {});
    
            console.log("Converted Leads Fresh Response:", result);
    
            if (result && Array.isArray(result.converted_leads)) {
                this.state.converted_leads = result.converted_leads;
                this.state.total_converted_leads = result.converted_leads.reduce((sum, item) => sum + item.count, 0);
                this.state.converted_leads_ids = result.converted_lead_ids;

            } else {
                console.error("Converted leads is not an array:", result.converted_leads);
            }
        } catch (error) {
            console.error("Error fetching Converted leads:", error);
        }
    }

    async fetchDeadDeclinedLeads() {
        try {
            const result = await rpc('/crm_dashboard/get_dead_declined', {});
            
            console.log("Dead Declined Leads API Response:", result);
            
            if (result && Array.isArray(result.dead_leads)) {  // ✅ Ensure it's an array
                this.state.dead_leads = result.dead_leads;
                this.state.total_dead_leads = result.dead_leads.reduce((sum, item) => sum + item.count, 0);
                this.state.dead_leads_ids = result.dead_leads_ids

            } else {
                console.error("Dead Declined leads is not an array:", result.dead_leads);
            }
        } catch (error) {
            console.error("Error fetching Dead Declined leads:", error);
        }
    }
    // _________________ Processing Daily Count Dashboard _________________________
    async fetchConsultationProcessing() {
        try {
            const result = await rpc('/crm_dashboard/get_consultation_processing', {});
            if (result && result.consultation_processing) {
                this.state.consultation_processing = result.consultation_processing;
                this.state.total_consultation_processing = result.consultation_processing.reduce((sum, stage) => sum + stage.count, 0);
                this.state.consultation_processing_ids = result.consultation_processing_ids;
            } 
        } catch (error) {
            console.error("Error fetching Consultation Processing:", error);
        }
    }
    
    
    async fetchApplicationInProcess() {
        try {
            const result = await rpc('/crm_dashboard/get_application_in_process', {});
            if (result && result.application_in_process) {
                this.state.application_in_process = result.application_in_process;
                this.state.total_application_in_process = result.application_in_process.reduce((sum, stage) => sum + stage.count, 0);
                this.state.application_in_process_ids = result.application_in_process_ids;
            } 
        } catch (error) {
            console.error("Error fetching Application In Process Processing:", error);
        }
    }
    
    
    async fetchFreezeProcessing() {
        try {
            const result = await rpc('/crm_dashboard/get_freeze_processing', {});
            if (result && result.freeze_processing) {
                this.state.freeze_processing = result.freeze_processing;
                this.state.total_freeze_processing = result.freeze_processing.reduce((sum, stage) => sum + stage.count, 0);
                this.state.freeze_processing_ids = result.freeze_processing_ids;
            } 
        } catch (error) {
            console.error("Error fetching Freeze Processing:", error);
        }
    }
    
    
    async fetchProcessing() {
        try {
            const result = await rpc('/crm_dashboard/get_processing', {});
            if (result && result.processing) {
                this.state.processing = result.processing;
                this.state.total_processing = result.processing.reduce((sum, stage) => sum + stage.count, 0);
                this.state.processing_ids = result.processing_ids;
            } 
        } catch (error) {
            console.error("Error fetching Processing:", error);
        }
    }


    async fetchAddLender() {
        try {
            const result = await rpc('/crm_dashboard/get_add_lender', {});
            if (result && result.add_lender) {
                this.state.add_lender = result.add_lender;
                this.state.total_add_lender = result.add_lender.reduce((sum, stage) => sum + stage.count, 0);
                this.state.add_lender_ids = result.add_lender_ids;
            } 
        } catch (error) {
            console.error("Error add lender Processing:", error);
        }
    }


    async fetchSubmittingDocs() {
        try {
            const result = await rpc('/crm_dashboard/get_submitting_docs', {});
            if (result && result.submitting_docs) {
                this.state.submitting_docs = result.submitting_docs;
                this.state.total_submitting_docs = result.submitting_docs.reduce((sum, stage) => sum + stage.count, 0);
                this.state.submitting_docs_ids = result.submitting_docs_ids;
            } 
        } catch (error) {
            console.error("Error submitting docs Processing:", error);
        }
    }


    async fetchSignedClosingDocs() {
        try {
            const result = await rpc('/crm_dashboard/get_signed_closing_docs', {});
            if (result && result.signed_closing_docs) {
                this.state.signed_closing_docs = result.signed_closing_docs;
                this.state.total_signed_closing_docs = result.signed_closing_docs.reduce((sum, stage) => sum + stage.count, 0);
                this.state.signed_closing_docs_ids = result.signed_closing_docs_ids;
            } 
        } catch (error) {
            console.error("Error submitting docs Processing:", error);
        }
    }


    async fetchPendingProcessing() {
        try {
            const result = await rpc('/crm_dashboard/get_pending_processing', {});
            if (result && result.pending_processing) {
                this.state.pending_processing = result.pending_processing;
                this.state.total_pending_processing = result.pending_processing.reduce((sum, stage) => sum + stage.count, 0);
                this.state.pending_processing_ids = result.pending_processing_ids;
            } 
        } catch (error) {
            console.error("Error Pending Processing:", error);
        }
    }
    


    // Bilal start working form here  Drildown functionality
    on_reverse_breadcrumb() {
        var self = this;
        WebClient.do_push_state({});
        this.update_cp();
        this.fetch_data().then(function() {
            self.$('.o_hr_dashboard').reload();
            self.render_dashboards();
        });
    }

    drilldown_function(e,lead_ids,page_name) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.action.doAction({
            name: _t(page_name),
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            view_mode: 'tree,form,calendar',
            views: [
                [false, 'list'],
                [false, 'form']
            ],
            domain: [
                ['id', 'in', lead_ids ],
            ],
            target: 'current',
        }, options)
    }

            //-----------------------(1st Dashboard) Daily count dashboard Ending ---------------------


            //---------------------- Owner Sales Dashboard ----------------------------

    async print_pdf(ev) {
        if (ev) {
            ev.preventDefault();
        }
        // console.log('🟢 DASHBOARD DATA:', dashboardData);
        this.action.doAction({
            type: 'ir.actions.report',
            report_name: 'crm_custom_dashboard.report_weekly_sales_pdf',
            report_type: 'qweb-pdf',
            data: {
                // weekly_sales_rep_dashboard:[
                //     {'user_name': e.user_name},
                // ]
                 weekly_sales_rep_dashboard: this.state.weekly_sales_rep_dashboard,
                 state: {
                    totalCrmLeads: this.state.totalCrmLeads,
                    totalLiveLeads: this.state.totalLiveLeads,
                    totalPortalLeads: this.state.totalPortalLeads,
                    totalCrmDuplicates: this.state.totalCrmDuplicates,
                    totalCrmDuplicatesPer: this.state.totalCrmDuplicatesPer,
                    totalCrmDnmc: this.state.totalCrmDnmc,
                    totalCrmDnmcPer: this.state.totalCrmDnmcPer,
                    totalCrmWorkable: this.state.totalCrmWorkable,
                    totalCrmWorkablePer: this.state.totalCrmWorkablePer,
                    totalCrmDeclinedLead: this.state.totalCrmDeclinedLead,
                    totalCrmDeclinedLeadPer: this.state.totalCrmDeclinedLeadPer,
                    totalCrmDncLead: this.state.totalCrmDncLead,
                    totalCrmDncLeadPer: this.state.totalCrmDncLeadPer,
                    totalCrmTransferredLead: this.state.totalCrmTransferredLead,
                    totalCrmTransferredLeadPer: this.state.totalCrmTransferredLeadPer,
                    totalCrmNoContactLead: this.state.totalCrmNoContactLead,
                    totalCrmNoContactLeadPer: this.state.totalCrmNoContactLeadPer,
                    totalCrmNoResponseLead: this.state.totalCrmNoResponseLead,
                    totalCrmNoResponseLeadPer: this.state.totalCrmNoResponseLeadPer,
                    totalPrimeLead: this.state.totalPrimeLead,
                    totalSubPrimeLead: this.state.totalSubPrimeLead,
                    totalPrimeDupLead: this.state.totalPrimeDupLead,
                    totalSubPrimeDupLead: this.state.totalSubPrimeDupLead,
                    totalPrimeDnmcLead: this.state.totalPrimeDnmcLead,
                    totalSubPrimeDnmcLead: this.state.totalSubPrimeDnmcLead,
                    totalPrimeWorkableLead: this.state.totalPrimeWorkableLead,
                    totalSubPrimeWorkableLead: this.state.totalSubPrimeWorkableLead,
                    totalPrimeDeclinedLead: this.state.totalPrimeDeclinedLead,
                    totalSubPrimeDeclinedLead: this.state.totalSubPrimeDeclinedLead,
                    totalPrimeDncLead: this.state.totalPrimeDncLead,
                    totalSubPrimeDncLead: this.state.totalSubPrimeDncLead,
                    totalPrimeTransferredLead: this.state.totalPrimeTransferredLead,
                    totalSubPrimeTransferredLead: this.state.totalSubPrimeTransferredLead,
                    totalPrimeNoContactLead: this.state.totalPrimeNoContactLead,
                    totalSubPrimeNoContactLead: this.state.totalSubPrimeNoContactLead,
                    totalPrimeNoResponseLead: this.state.totalPrimeNoResponseLead,
                    totalSubPrimeNoResponseLead: this.state.totalSubPrimeNoResponseLead,
                }

            }
        });
        debugger;
        console.log("weekly_sales_rep_dashboard", this.state.weekly_sales_rep_dashboard)
        console.log("state values", this.state.totalCrmLeads)  // Should NOT be undefined

    }
    // weekly_sales_rep_dashboard: dashboardData.get_total_leads_new

    async fetchTotalLeads() {
        try {
            const return_data = []
            let totalLiveLeads = 0;
            let totalPortalLeads = 0;
            let totalCrmLeads = 0;
            let totalLiveDuplicates = 0;
            let totalPortalDuplicates = 0;
            let totalCrmDuplicates = 0;
            let totalCrmDuplicatesPer = 0;
            let totalLiveDnmc = 0;
            let totalPortalDnmc = 0;
            let totalCrmDnmc = 0;
            let totalCrmDnmcPer = 0;
            let totalLiveWorkable = 0;
            let totalPortalWorkable = 0;
            let totalCrmWorkable = 0;
            let totalCrmWorkablePer = 0;
            let totalLiveDeclinedLead = 0;
            let totalPortalDeclinedLead = 0;
            let totalCrmDeclinedLead = 0;
            let totalCrmDeclinedLeadPer = 0;
            let totalLiveDncLead = 0;
            let totalPortalDncLead = 0;
            let totalCrmDncLead = 0;
            let totalCrmDncLeadPer = 0;
            let totalLiveTransferredLead = 0;
            let totalPortalTransferredLead = 0;
            let totalCrmTransferredLead = 0;
            let totalCrmTransferredLeadPer = 0;
            let totalLiveNoContactLead = 0;
            let totalPortalNoContactLead = 0;
            let totalCrmNoContactLead = 0;
            let totalCrmNoContactLeadPer = 0;
            let totalLiveNoResponseLead = 0;
            let totalPortalNoResponseLead = 0;
            let totalCrmNoResponseLead = 0;
            let totalCrmNoResponseLeadPer = 0;
            let totalPrimeLead = 0;
            let totalSubPrimeLead = 0;
            let totalPrimeDupLead = 0;
            let totalSubPrimeDupLead = 0;
            let totalPrimeDnmcLead = 0;
            let totalSubPrimeDnmcLead = 0;
            let totalPrimeWorkableLead = 0;
            let totalSubPrimeWorkableLead = 0;
            let totalPrimeDeclinedLead = 0;
            let totalSubPrimeDeclinedLead = 0;
            let totalPrimeDncLead = 0;
            let totalSubPrimeDncLead = 0;
            let totalPrimeTransferredLead = 0;
            let totalSubPrimeTransferredLead = 0;
            let totalPrimeNoContactLead = 0;
            let totalSubPrimeNoContactLead = 0;
            let totalPrimeNoResponseLead = 0;
            let totalSubPrimeNoResponseLead = 0;

            const result = await rpc('/crm_dashboard/get_total_leads', {});
            if (result && result.get_total_leads_new) {
                console.log("result.get_total_leads_new", result)
                result.get_total_leads_new.forEach(async (e) => {

                    totalLiveLeads += e.total_live_lead || 0;
                    totalPortalLeads += e.total_portal_lead || 0;
                    totalCrmLeads += (e.total_live_lead || 0) + (e.total_portal_lead || 0);
                    totalLiveDuplicates += e.total_live_duplicate || 0;
                    totalPortalDuplicates += e.total_portal_duplicate || 0;
                    totalCrmDuplicates += (e.total_live_duplicate || 0) + (e.total_portal_duplicate || 0);
                    totalCrmDuplicatesPer = totalCrmLeads > 0 ? ((totalCrmDuplicates / totalCrmLeads) * 100).toFixed(2) : "0.00"; 
                    totalLiveDnmc += e.total_live_dnmc_lead || 0;
                    totalPortalDnmc += e.total_portal_dnmc_lead || 0;
                    totalCrmDnmc += (e.total_live_dnmc_lead || 0) + (e.total_portal_dnmc_lead || 0);
                    totalCrmDnmcPer = totalCrmLeads > 0 ? ((totalCrmDnmc / totalCrmLeads) * 100).toFixed(2) : "0.00";
                    totalLiveWorkable += e.total_live_workable || 0 ;
                    totalPortalWorkable += e.total_portal_workable || 0; 
                    totalCrmWorkable += (e.total_live_workable || 0) + (e.total_portal_workable || 0);
                    totalCrmWorkablePer = totalCrmLeads > 0 ? ((totalCrmWorkable / totalCrmLeads) * 100).toFixed(2) : "0.00";
                    totalLiveDeclinedLead += e.total_live_declined_lead || 0 ;
                    totalPortalDeclinedLead += e.total_portal_declined_lead || 0; 
                    totalCrmDeclinedLead += (e.total_live_declined_lead || 0) + (e.total_portal_declined_lead || 0);
                    totalCrmDeclinedLeadPer = totalCrmWorkable > 0 ? ((totalCrmDeclinedLead / totalCrmWorkable) * 100).toFixed(2) : "0.00";
                    totalLiveDncLead += e.total_live_dnc_lead || 0 ;
                    totalPortalDncLead += e.total_portal_dnc_lead || 0; 
                    totalCrmDncLead += (e.total_live_dnc_lead || 0) + (e.total_portal_dnc_lead || 0);
                    totalCrmDncLeadPer = totalCrmWorkable > 0 ? ((totalCrmDncLead / totalCrmWorkable) * 100).toFixed(2) : "0.00";
                    totalLiveTransferredLead += e.total_live_transferred_lead || 0 ;
                    totalPortalTransferredLead += e.total_portal_transferred_lead || 0; 
                    totalCrmTransferredLead += (e.total_live_transferred_lead || 0) + (e.total_portal_transferred_lead || 0); 
                    totalCrmTransferredLeadPer = totalCrmWorkable > 0 ? ((totalCrmTransferredLead / totalCrmWorkable) * 100).toFixed(2) : "0.00";
                    totalLiveNoContactLead += e.total_live_no_contact_lead || 0 ;
                    totalPortalNoContactLead += e.total_portal_no_contact_lead || 0; 
                    totalCrmNoContactLead += (e.total_live_no_contact_lead || 0) + (e.total_portal_no_contact_lead || 0); 
                    totalCrmNoContactLeadPer = totalCrmWorkable > 0 ? ((totalCrmNoContactLead / totalCrmWorkable) * 100).toFixed(2) : "0.00";
                    totalLiveNoResponseLead += e.total_live_no_response_lead || 0 ;
                    totalPortalNoResponseLead += e.total_portal_no_response_lead || 0; 
                    totalCrmNoResponseLead += (e.total_live_no_response_lead || 0) + (e.total_portal_no_response_lead || 0); 
                    totalCrmNoResponseLeadPer = totalCrmWorkable > 0 ? ((totalCrmNoResponseLead / totalCrmWorkable) * 100).toFixed(2) : "0.00";
                    totalPrimeLead += e.total_prime_lead || 0;
                    totalSubPrimeLead += e.total_subprime_lead || 0;
                    totalPrimeDupLead += e.total_prime_dup_lead || 0;
                    totalSubPrimeDupLead += e.total_subprime_dup_lead || 0;
                    totalPrimeDnmcLead += e.total_prime_dnmc_lead || 0;
                    totalSubPrimeDnmcLead += e.total_subprime_dnmc_lead || 0;
                    totalPrimeWorkableLead += e.total_prime_workable_lead || 0;
                    totalSubPrimeWorkableLead += e.total_subprime_workable_lead || 0;
                    totalPrimeDeclinedLead += e.total_prime_declined_lead || 0;
                    totalSubPrimeDeclinedLead += e.total_subprime_declined_lead || 0;
                    totalPrimeDncLead += e.total_prime_dnc_lead || 0;
                    totalSubPrimeDncLead += e.total_subprime_dnc_lead || 0;
                    totalPrimeTransferredLead += e.total_prime_transferred_lead || 0;
                    totalSubPrimeTransferredLead += e.total_subprime_transferred_lead || 0;
                    totalPrimeNoContactLead += e.total_prime_no_contact_lead || 0;
                    totalSubPrimeNoContactLead += e.total_subprime_no_contact_lead || 0;
                    totalPrimeNoResponseLead += e.total_prime_no_response_lead || 0;
                    totalSubPrimeNoResponseLead += e.total_subprime_no_response_lead || 0;
                    return_data.push({
                        'user_id': e.user_id,
                        'user_name': e.user_name,
                        'total_leads_data': 0,
                        'total_crm_leads': e.total_live_lead + e.total_portal_lead,
                        'total_live_leads': e.total_live_lead,
                        'live_leads_ids':e.live_leads_ids,
                        'portal_leads_ids':e.portal_leads_ids,
                        'combined_leads_ids' :e.combined_leads_ids,
                        'total_portal_leads': e.total_portal_lead,
                        'total_live_duplicates': e.total_live_duplicate,
                        'total_live_duplicates_per': e.total_live_lead > 0 ? ((e.total_live_duplicate / e.total_live_lead) * 100).toFixed(2) : '0.00',
                        'live_duplicates_ids': e.live_duplicates_ids,
                        'portal_duplicates_ids': e.portal_duplicates_ids,
                        'total_portal_duplicates': e.total_portal_duplicate,
                        'total_portal_duplicates_per': e.total_portal_lead > 0 ? ((e.total_portal_duplicate / e.total_portal_lead) * 100).toFixed(2) : '0.00',
                        'total_live_dnmc_leads': e.total_live_dnmc_lead,
                        'total_live_dnmc_leads_per': e.total_live_lead > 0 ? ((e.total_live_dnmc_lead / e.total_live_lead) * 100).toFixed(2) : '0.00',
                        'live_dnmc_lead_ids': e.live_dnmc_lead_ids,
                        'portal_dnmc_lead_ids': e.portal_dnmc_lead_ids,
                        'total_portal_dnmc_leads': e.total_portal_dnmc_lead,
                        'total_portal_dnmc_leads_per': e.total_portal_lead > 0 ? ((e.total_portal_dnmc_lead / e.total_portal_lead) * 100).toFixed(2) : '0.00',
                        'total_live_workables': e.total_live_workable,
                        'total_live_workables_per': e.total_live_lead > 0 ? ((e.total_live_workable / e.total_live_lead) * 100).toFixed(2) : '0.00',
                        'live_workable_ids': e.live_workable_ids,
                        'portal_workable_ids': e.portal_workable_ids,
                        'total_portal_workables': e.total_portal_workable,
                        'total_portal_workables_per': e.total_portal_lead > 0 ? ((e.total_portal_workable / e.total_portal_lead) * 100).toFixed(2) : '0.00',
                        'total_workable_ids': e.total_workable_ids,
                        'total_workables': e.total_workable_lead,
                        'total_live_declined_leads': e.total_live_declined_lead,
                        'total_live_declined_leads_per': e.total_live_workable > 0 ? ((e.total_live_declined_lead / e.total_live_workable) * 100).toFixed(2) : '0.00',
                        'live_declined_lead_ids': e.live_declined_lead_ids,
                        'portal_declined_lead_ids': e.portal_declined_lead_ids,
                        'total_portal_declined_leads': e.total_portal_declined_lead,
                        'total_portal_declined_leads_per': e.total_portal_workable > 0 ? ((e.total_portal_declined_lead / e.total_portal_workable) * 100).toFixed(2) : '0.00',
                        'total_live_dnc_leads': e.total_live_dnc_lead,
                        'total_live_dnc_leads_per': e.total_live_workable > 0 ? ((e.total_live_dnc_lead / e.total_live_workable) * 100).toFixed(2) : '0.00',
                        'live_dnc_lead_ids': e.live_dnc_lead_ids,
                        'portal_dnc_lead_ids': e.portal_dnc_lead_ids,
                        'total_portal_dnc_leads': e.total_portal_dnc_lead,
                        'total_portal_dnc_leads_per': e.total_portal_workable > 0 ? ((e.total_portal_dnc_lead / e.total_portal_workable) * 100).toFixed(2) : '0.00',
                        'total_live_transferred_leads': e.total_live_transferred_lead,
                        'total_live_transferred_leads_per': e.total_live_workable > 0 ? ((e.total_live_transferred_lead / e.total_live_workable) * 100).toFixed(2) : '0.00',
                        'live_transferred_lead_ids': e.live_transferred_lead_ids,
                        'portal_transferred_lead_ids': e.portal_transferred_lead_ids,
                        'total_portal_transferred_leads': e.total_portal_transferred_lead,
                        'total_portal_transferred_leads_per': e.total_portal_workable > 0 ? ((e.total_portal_transferred_lead / e.total_portal_workable) * 100).toFixed(2) : '0.00',
                        'total_live_no_contact_leads': e.total_live_no_contact_lead,
                        'total_live_no_contact_leads_per': e.total_live_workable > 0 ? ((e.total_live_no_contact_lead / e.total_live_workable) * 100).toFixed(2) : '0.00',
                        'live_no_contact_lead_ids': e.live_no_contact_lead_ids,
                        'portal_no_contact_lead_ids': e.portal_no_contact_lead_ids,
                        'total_portal_no_contact_leads': e.total_portal_no_contact_lead,
                        'total_portal_no_contact_leads_per': e.total_portal_workable > 0 ? ((e.total_portal_no_contact_lead / e.total_portal_workable) * 100).toFixed(2) : '0.00',
                        'total_live_no_response_leads': e.total_live_no_response_lead,
                        'total_live_no_response_leads_per': e.total_live_workable > 0 ? ((e.total_live_no_response_lead / e.total_live_workable) * 100).toFixed(2) : '0.00',
                        'live_no_response_lead_ids': e.live_no_response_lead_ids,
                        'portal_no_response_lead_ids': e.portal_no_response_lead_ids,
                        'total_portal_no_response_leads': e.total_portal_no_response_lead,
                        'total_portal_no_response_leads_per': e.total_portal_workable > 0 ? ((e.total_portal_no_response_lead / e.total_portal_workable) * 100).toFixed(2) : '0.00',
                        'total_live_deal_leads': e.total_live_deal_lead,
                        'live_deal_lead_ids': e.live_deal_lead_ids,
                        'portal_deal_lead_ids': e.portal_deal_lead_ids,
                        'total_portal_deal_leads': e.total_portal_deal_lead,
                        'total_prime_lead' : e.total_prime_lead,
                        'total_subprime_lead' : e.total_subprime_lead,
                        'total_prime_dup_lead' : e.total_prime_dup_lead,
                        'total_subprime_dup_lead' : e.total_subprime_dup_lead,
                        'total_prime_dnmc_lead' : e.total_prime_dnmc_lead,
                        'total_subprime_dnmc_lead' : e.total_subprime_dnmc_lead,
                        'total_prime_workable_lead' : e.total_prime_workable_lead,
                        'total_subprime_workable_lead' : e.total_subprime_workable_lead,
                        'total_prime_declined_lead' : e.total_prime_declined_lead,
                        'total_subprime_declined_lead' : e.total_subprime_declined_lead,
                        'total_prime_dnc_lead' : e.total_prime_dnc_lead,
                        'total_subprime_dnc_lead' : e.total_subprime_dnc_lead,
                        'total_prime_transferred_lead' : e.total_prime_transferred_lead,
                        'total_subprime_transferred_lead' : e.total_subprime_transferred_lead,
                        'total_prime_no_contact_lead' : e.total_prime_no_contact_lead,
                        'total_subprime_no_contact_lead' : e.total_subprime_no_contact_lead,
                        'total_prime_no_response_lead' : e.total_prime_no_response_lead,
                        'total_subprime_no_response_lead' : e.total_subprime_no_response_lead,
                    })
                    
                });
                console.log("Bilal console",result.get_total_leads_new)
                this.state.weekly_sales_rep_dashboard = return_data
                this.state.totalLiveLeads = totalLiveLeads;
                this.state.totalPortalLeads = totalPortalLeads;
                this.state.totalCrmLeads = totalCrmLeads;
                this.state.totalLiveDuplicates = totalLiveDuplicates;
                this.state.totalPortalDuplicates = totalPortalDuplicates;
                this.state.totalCrmDuplicates = totalCrmDuplicates;
                this.state.totalCrmDuplicatesPer = totalCrmDuplicatesPer;
                this.state.totalLiveDnmc = totalLiveDnmc;
                this.state.totalPortalDnmc = totalPortalDnmc;
                this.state.totalCrmDnmc = totalCrmDnmc;
                this.state.totalCrmDnmcPer = totalCrmDnmcPer;
                this.state.totalLiveWorkable = totalLiveWorkable;
                this.state.totalPortalWorkable = totalPortalWorkable;
                this.state.totalCrmWorkable = totalCrmWorkable;
                this.state.totalCrmWorkablePer = totalCrmWorkablePer;
                this.state.totalLiveDeclinedLead = totalLiveDeclinedLead;
                this.state.totalPortalDeclinedLead = totalPortalDeclinedLead;
                this.state.totalCrmDeclinedLead = totalCrmDeclinedLead;
                this.state.totalCrmDeclinedLeadPer = totalCrmDeclinedLeadPer;
                this.state.totalLiveDncLead = totalLiveDncLead;
                this.state.totalPortalDncLead = totalPortalDncLead;
                this.state.totalCrmDncLead = totalCrmDncLead;
                this.state.totalCrmDncLeadPer = totalCrmDncLeadPer;
                this.state.totalLiveTransferredLead = totalLiveTransferredLead;
                this.state.totalPortalTransferredLead = totalPortalTransferredLead;
                this.state.totalCrmTransferredLead = totalCrmTransferredLead;
                this.state.totalCrmTransferredLeadPer = totalCrmTransferredLeadPer;
                this.state.totalLiveNoContactLead = totalLiveNoContactLead;
                this.state.totalPortalNoContactLead = totalPortalNoContactLead;
                this.state.totalCrmNoContactLead = totalCrmNoContactLead;
                this.state.totalCrmNoContactLeadPer = totalCrmNoContactLeadPer;
                this.state.totalLiveNoResponseLead = totalLiveNoResponseLead;
                this.state.totalPortalNoResponseLead = totalPortalNoResponseLead;
                this.state.totalCrmNoResponseLead = totalCrmNoResponseLead;
                this.state.totalCrmNoResponseLeadPer = totalCrmNoResponseLeadPer;
                this.state.totalPrimeLead = totalPrimeLead;
                this.state.totalSubPrimeLead = totalSubPrimeLead;
                this.state.totalPrimeDupLead = totalPrimeDupLead;
                this.state.totalSubPrimeDupLead = totalSubPrimeDupLead;
                this.state.totalPrimeDnmcLead = totalPrimeDnmcLead;
                this.state.totalSubPrimeDnmcLead = totalSubPrimeDnmcLead;
                this.state.totalPrimeWorkableLead = totalPrimeWorkableLead;
                this.state.totalSubPrimeWorkableLead = totalSubPrimeWorkableLead;
                this.state.totalPrimeDeclinedLead = totalPrimeDeclinedLead;
                this.state.totalSubPrimeDeclinedLead = totalSubPrimeDeclinedLead;
                this.state.totalPrimeDncLead = totalPrimeDncLead;
                this.state.totalSubPrimeDncLead = totalSubPrimeDncLead;
                this.state.totalPrimeTransferredLead = totalPrimeTransferredLead;
                this.state.totalSubPrimeTransferredLead = totalSubPrimeTransferredLead;
                this.state.totalPrimeNoContactLead = totalPrimeNoContactLead;
                this.state.totalSubPrimeNoContactLead = totalSubPrimeNoContactLead;
                this.state.totalPrimeNoResponseLead = totalPrimeNoResponseLead;
                this.state.totalSubPrimeNoResponseLead = totalSubPrimeNoResponseLead;


            }
            console.log(return_data)
            

        } catch (error) {
            console.error("Error fetching New leads:", error);
        }
    }
                                    // Owner Dashboard Ending
                
                
                                    // Affiliate Sales Dashboard Starting
    async fetchTotalSalesLeads() {
        try {
            const return_data = []
            let affiliatetotalLiveLeads = 0;
            let affiliatetotalPortalLeads = 0;
            let affiliatetotalCrmLeads = 0;
            let affiliatetotalLiveDuplicates = 0;
            let affiliatetotalPortalDuplicates = 0;
            let affiliatetotalCrmDuplicates = 0;
            let affiliatetotalCrmDuplicatesPer = 0;
            let affiliatetotalLiveDnmc = 0;
            let affiliatetotalPortalDnmc = 0;
            let affiliatetotalCrmDnmc = 0;
            let affiliatetotalCrmDnmcPer = 0;
            let affiliatetotalLiveWorkable = 0;
            let affiliatetotalPortalWorkable = 0;
            let affiliatetotalCrmWorkable = 0;
            let affiliatetotalCrmWorkablePer = 0;
            let affiliatetotalLiveDeclinedLead = 0;
            let affiliatetotalPortalDeclinedLead = 0;
            let affiliatetotalCrmDeclinedLead = 0;
            let affiliatetotalCrmDeclinedLeadPer = 0;
            let affiliatetotalLiveDncLead = 0;
            let affiliatetotalPortalDncLead = 0;
            let affiliatetotalCrmDncLead = 0;
            let affiliatetotalCrmDncLeadPer = 0;
            let affiliatetotalLiveTransferredLead = 0;
            let affiliatetotalPortalTransferredLead = 0;
            let affiliatetotalCrmTransferredLead = 0;
            let affiliatetotalCrmTransferredLeadPer = 0;
            let affiliatetotalLiveNoContactLead = 0;
            let affiliatetotalPortalNoContactLead = 0;
            let affiliatetotalCrmNoContactLead = 0;
            let affiliatetotalCrmNoContactLeadPer = 0;
            let affiliatetotalLiveNoResponseLead = 0;
            let affiliatetotalPortalNoResponseLead = 0;
            let affiliatetotalCrmNoResponseLead = 0;
            let affiliatetotalCrmNoResponseLeadPer = 0;
            let affiliatetotalPrimeLead = 0;
            let affiliatetotalSubPrimeLead = 0;
            let affiliatetotalPrimeDupLead = 0;
            let affiliatetotalSubPrimeDupLead = 0;
            let affiliatetotalPrimeDnmcLead = 0;
            let affiliatetotalSubPrimeDnmcLead = 0;
            let affiliatetotalPrimeWorkableLead = 0;
            let affiliatetotalSubPrimeWorkableLead = 0;
            let affiliatetotalPrimeDeclinedLead = 0;
            let affiliatetotalSubPrimeDeclinedLead = 0;
            let affiliatetotalPrimeDncLead = 0;
            let affiliatetotalSubPrimeDncLead = 0;
            let affiliatetotalPrimeTransferredLead = 0;
            let affiliatetotalSubPrimeTransferredLead = 0;
            let affiliatetotalPrimeNoContactLead = 0;
            let affiliatetotalSubPrimeNoContactLead = 0;
            let affiliatetotalPrimeNoResponseLead = 0;
            let affiliatetotalSubPrimeNoResponseLead = 0;
            
            const result = await rpc('/crm_dashboard/get_total_crm_lead', {});
            console.log("result.total_crm_leads_data", result)
            if (result && result.total_crm_leads_data) {
                console.log("result.total_crm_leads_data affiliate", result)
                result.total_crm_leads_data.forEach(async (e) => {
                    // for (const e of result.total_crm_leads_data) {
                        
                    affiliatetotalLiveLeads += e.total_live_lead || 0;
                    affiliatetotalPortalLeads += e.total_portal_lead || 0;
                    affiliatetotalCrmLeads += (e.total_live_lead || 0) + (e.total_portal_lead || 0);
                    affiliatetotalLiveDuplicates += e.total_live_duplicate || 0;
                    affiliatetotalPortalDuplicates += e.total_portal_duplicate || 0;
                    affiliatetotalCrmDuplicates += (e.total_live_duplicate || 0) + (e.total_portal_duplicate || 0);
                    affiliatetotalCrmDuplicatesPer = affiliatetotalCrmLeads > 0 ? ((affiliatetotalCrmDuplicates / affiliatetotalCrmLeads) * 100).toFixed(2) : "0.00"; 
                    affiliatetotalLiveDnmc += e.total_live_dnmc_lead || 0;
                    affiliatetotalPortalDnmc += e.total_portal_dnmc_lead || 0;
                    affiliatetotalCrmDnmc += (e.total_live_dnmc_lead || 0) + (e.total_portal_dnmc_lead || 0);
                    affiliatetotalCrmDnmcPer =affiliatetotalCrmLeads > 0 ? ((affiliatetotalCrmDnmc / affiliatetotalCrmLeads) * 100).toFixed(2) : "0.00";
                    affiliatetotalLiveWorkable += e.total_live_workable || 0 ;
                    affiliatetotalPortalWorkable += e.total_portal_workable || 0; 
                    affiliatetotalCrmWorkable += (e.total_live_workable || 0) + (e.total_portal_workable || 0);
                    affiliatetotalCrmWorkablePer = affiliatetotalCrmLeads > 0 ? ((affiliatetotalCrmWorkable / affiliatetotalCrmLeads) * 100).toFixed(2) : "0.00";
                    affiliatetotalLiveDeclinedLead += e.total_live_declined_lead || 0 ;
                    affiliatetotalPortalDeclinedLead += e.total_portal_declined_lead || 0; 
                    affiliatetotalCrmDeclinedLead += (e.total_live_declined_lead || 0) + (e.total_portal_declined_lead || 0);
                    affiliatetotalCrmDeclinedLeadPer = affiliatetotalCrmWorkable > 0 ? ((affiliatetotalCrmDeclinedLead / affiliatetotalCrmWorkable) * 100).toFixed(2) : "0.00";
                    affiliatetotalLiveDncLead += e.total_live_dnc_lead || 0 ;
                    affiliatetotalPortalDncLead += e.total_portal_dnc_lead || 0; 
                    affiliatetotalCrmDncLead += (e.total_live_dnc_lead || 0) + (e.total_portal_dnc_lead || 0);
                    affiliatetotalCrmDncLeadPer = affiliatetotalCrmWorkable > 0 ? ((affiliatetotalCrmDncLead / affiliatetotalCrmWorkable) * 100).toFixed(2) : "0.00";
                    affiliatetotalLiveTransferredLead += e.total_live_transferred_lead || 0 ;
                    affiliatetotalPortalTransferredLead += e.total_portal_transferred_lead || 0; 
                    affiliatetotalCrmTransferredLead += (e.total_live_transferred_lead || 0) + (e.total_portal_transferred_lead || 0); 
                    affiliatetotalCrmTransferredLeadPer = affiliatetotalCrmWorkable > 0 ? ((affiliatetotalCrmTransferredLead / affiliatetotalCrmWorkable) * 100).toFixed(2) : "0.00";
                    affiliatetotalLiveNoContactLead += e.total_live_no_contact_lead || 0 ;
                    affiliatetotalPortalNoContactLead += e.total_portal_no_contact_lead || 0; 
                    affiliatetotalCrmNoContactLead += (e.total_live_no_contact_lead || 0) + (e.total_portal_no_contact_lead || 0); 
                    affiliatetotalCrmNoContactLeadPer = affiliatetotalCrmWorkable > 0 ? ((affiliatetotalCrmNoContactLead / affiliatetotalCrmWorkable) * 100).toFixed(2) : "0.00";
                    affiliatetotalLiveNoResponseLead += e.total_live_no_response_lead || 0 ;
                    affiliatetotalPortalNoResponseLead += e.total_portal_no_response_lead || 0; 
                    affiliatetotalCrmNoResponseLead += (e.total_live_no_response_lead || 0) + (e.total_portal_no_response_lead || 0); 
                    affiliatetotalCrmNoResponseLeadPer = affiliatetotalCrmWorkable > 0 ? ((affiliatetotalCrmNoResponseLead / affiliatetotalCrmWorkable) * 100).toFixed(2) : "0.00";
                    affiliatetotalPrimeLead += e.total_prime_lead || 0;
                    affiliatetotalSubPrimeLead += e.total_subprime_lead || 0;
                    affiliatetotalPrimeDupLead += e.total_prime_dup_lead || 0;
                    affiliatetotalSubPrimeDupLead += e.total_subprime_dup_lead || 0;
                    affiliatetotalPrimeDnmcLead += e.total_prime_dnmc_lead || 0;
                    affiliatetotalSubPrimeDnmcLead += e.total_subprime_dnmc_lead || 0;
                    affiliatetotalPrimeWorkableLead += e.total_prime_workable_lead || 0;
                    affiliatetotalSubPrimeWorkableLead += e.total_subprime_workable_lead || 0;
                    affiliatetotalPrimeDeclinedLead += e.total_prime_declined_lead || 0;
                    affiliatetotalSubPrimeDeclinedLead += e.total_subprime_declined_lead || 0;
                    affiliatetotalPrimeDncLead += e.total_prime_dnc_lead || 0;
                    affiliatetotalSubPrimeDncLead += e.total_subprime_dnc_lead || 0;
                    affiliatetotalPrimeTransferredLead += e.total_prime_transferred_lead || 0;
                    affiliatetotalSubPrimeTransferredLead += e.total_subprime_transferred_lead || 0;
                    affiliatetotalPrimeNoContactLead += e.total_prime_no_contact_lead || 0;
                    affiliatetotalSubPrimeNoContactLead += e.total_subprime_no_contact_lead || 0;
                    affiliatetotalPrimeNoResponseLead += e.total_prime_no_response_lead || 0;
                    affiliatetotalSubPrimeNoResponseLead += e.total_subprime_no_response_lead || 0;
                    
                    return_data.push({
                        'user_id': e.user_id,
                        'user_name': e.user_name,
                        'total_leads_data': 0,
                        'total_crm_leads': e.total_live_lead + e.total_portal_lead,
                        'total_live_leads': e.total_live_lead,
                        'live_leads_ids':e.live_leads_ids,
                        'portal_leads_ids':e.portal_leads_ids,
                        'combined_leads_ids':e.combined_leads_ids,
                        'total_portal_leads': e.total_portal_lead,
                        'total_live_duplicates': e.total_live_duplicate,
                        'total_live_duplicates_per': e.total_live_lead > 0 ? ((e.total_live_duplicate / e.total_live_lead) * 100).toFixed(2) : '0.00',
                        'live_duplicates_ids': e.live_duplicates_ids,
                        'portal_duplicates_ids': e.portal_duplicates_ids,
                        'total_portal_duplicates': e.total_portal_duplicate,
                        'total_portal_duplicates_per': e.total_portal_lead > 0 ? ((e.total_portal_duplicate / e.total_portal_lead) * 100).toFixed(2) : '0.00',
                        'total_live_dnmc_leads': e.total_live_dnmc_lead,
                        'total_live_dnmc_leads_per': e.total_live_lead > 0 ? ((e.total_live_dnmc_lead / e.total_live_lead) * 100).toFixed(2) : '0.00',
                        'live_dnmc_lead_ids': e.live_dnmc_lead_ids,
                        'portal_dnmc_lead_ids': e.portal_dnmc_lead_ids,
                        'total_portal_dnmc_leads': e.total_portal_dnmc_lead,
                        'total_portal_dnmc_leads_per': e.total_portal_lead > 0 ? ((e.total_portal_dnmc_lead / e.total_portal_lead) * 100).toFixed(2) : '0.00',
                        'total_live_workables': e.total_live_workable,
                        'total_live_workables_per': e.total_live_lead > 0 ? ((e.total_live_workable / e.total_live_lead) * 100).toFixed(2) : '0.00',
                        'live_workable_ids': e.live_workable_ids,
                        'portal_workable_ids': e.portal_workable_ids,
                        'total_portal_workables': e.total_portal_workable,
                        'total_portal_workables_per': e.total_portal_lead > 0 ? ((e.total_portal_workable / e.total_portal_lead) * 100).toFixed(2) : '0.00',
                        'total_workables': e.total_workable_lead,
                        'total_workable_ids' : e.total_workable_ids,
                        'total_live_declined_leads': e.total_live_declined_lead,
                        'total_live_declined_leads_per': e.total_live_workable > 0 ? ((e.total_live_declined_lead / e.total_live_workable) * 100).toFixed(2) : '0.00',
                        'live_declined_lead_ids': e.live_declined_lead_ids,
                        'portal_declined_lead_ids': e.portal_declined_lead_ids,
                        'total_portal_declined_leads': e.total_portal_declined_lead,
                        'total_portal_declined_leads_per': e.total_portal_workable > 0 ? ((e.total_portal_declined_lead / e.total_portal_workable) * 100).toFixed(2) : '0.00',
                        'total_live_dnc_leads': e.total_live_dnc_lead,
                        'total_live_dnc_leads_per': e.total_live_workable > 0 ? ((e.total_live_dnc_lead / e.total_live_workable) * 100).toFixed(2) : '0.00',
                        'live_dnc_lead_ids': e.live_dnc_lead_ids,
                        'portal_dnc_lead_ids': e.portal_dnc_lead_ids,
                        'total_portal_dnc_leads': e.total_portal_dnc_lead,
                        'total_portal_dnc_leads_per': e.total_portal_workable > 0 ? ((e.total_portal_dnc_lead / e.total_portal_workable) * 100).toFixed(2) : '0.00',
                        'total_live_transferred_leads': e.total_live_transferred_lead,
                        'total_live_transferred_leads_per': e.total_live_workable > 0 ? ((e.total_live_transferred_lead / e.total_live_workable) * 100).toFixed(2) : '0.00',
                        'live_transferred_lead_ids': e.live_transferred_lead_ids,
                        'portal_transferred_lead_ids': e.portal_transferred_lead_ids,
                        'total_portal_transferred_leads': e.total_portal_transferred_lead,
                        'total_portal_transferred_leads_per': e.total_portal_workable > 0 ? ((e.total_portal_transferred_lead / e.total_portal_workable) * 100).toFixed(2) : '0.00',
                        'total_live_no_contact_leads': e.total_live_no_contact_lead,
                        'total_live_no_contact_leads_per': e.total_live_workable > 0 ? ((e.total_live_no_contact_lead / e.total_live_workable) * 100).toFixed(2) : '0.00',
                        'live_no_contact_lead_ids': e.live_no_contact_lead_ids,
                        'portal_no_contact_lead_ids': e.portal_no_contact_lead_ids,
                        'total_portal_no_contact_leads': e.total_portal_no_contact_lead,
                        'total_portal_no_contact_leads_per': e.total_portal_workable > 0 ? ((e.total_portal_no_contact_lead / e.total_portal_workable) * 100).toFixed(2) : '0.00',
                        'total_live_no_response_leads': e.total_live_no_response_lead,
                        'total_live_no_response_leads_per': e.total_live_workable > 0 ? ((e.total_live_no_response_lead / e.total_live_workable) * 100).toFixed(2) : '0.00',
                        'live_no_response_lead_ids': e.live_no_response_lead_ids,
                        'portal_no_response_lead_ids': e.portal_no_response_lead_ids,
                        'total_portal_no_response_leads': e.total_portal_no_response_lead,
                        'total_portal_no_response_leads_per': e.total_portal_workable > 0 ? ((e.total_portal_no_response_lead / e.total_portal_workable) * 100).toFixed(2) : '0.00',
                        'total_live_deal_leads': e.total_live_deal_lead,
                        'live_deal_lead_ids': e.live_deal_lead_ids,
                        'portal_deal_lead_ids': e.portal_deal_lead_ids,
                        'total_portal_deal_leads': e.total_portal_deal_lead,
                        'total_prime_lead' : e.total_prime_lead,
                        'total_subprime_lead' : e.total_subprime_lead,
                        'total_prime_dup_lead' : e.total_prime_dup_lead,
                        'total_subprime_dup_lead' : e.total_subprime_dup_lead,
                        'total_prime_dnmc_lead' : e.total_prime_dnmc_lead,
                        'total_subprime_dnmc_lead' : e.total_subprime_dnmc_lead,
                        'total_prime_workable_lead' : e.total_prime_workable_lead,
                        'total_subprime_workable_lead' : e.total_subprime_workable_lead,
                        'total_prime_declined_lead' : e.total_prime_declined_lead,
                        'total_subprime_declined_lead' : e.total_subprime_declined_lead,
                        'total_prime_dnc_lead' : e.total_prime_dnc_lead,
                        'total_subprime_dnc_lead' : e.total_subprime_dnc_lead,
                        'total_prime_transferred_lead' : e.total_prime_transferred_lead,
                        'total_subprime_transferred_lead' : e.total_subprime_transferred_lead,
                        'total_prime_no_contact_lead' : e.total_prime_no_contact_lead,
                        'total_subprime_no_contact_lead' : e.total_subprime_no_contact_lead,
                        'total_prime_no_response_lead' : e.total_prime_no_response_lead,
                        'total_subprime_no_response_lead' : e.total_subprime_no_response_lead,
                    })
                    
                });
                console.log("console",result.total_crm_leads_data)
                this.state.affiliateweekly_sales_rep_dashboard = return_data
                this.state.affiliatetotalLiveLeads = affiliatetotalLiveLeads;
                this.state.affiliatetotalPortalLeads = affiliatetotalPortalLeads;
                this.state.affiliatetotalCrmLeads = affiliatetotalCrmLeads;
                this.state.affiliatetotalLiveDuplicates = affiliatetotalLiveDuplicates;
                this.state.affiliatetotalPortalDuplicates = affiliatetotalPortalDuplicates;
                this.state.affiliatetotalCrmDuplicates = affiliatetotalCrmDuplicates;
                this.state.affiliatetotalCrmDuplicatesPer = affiliatetotalCrmDuplicatesPer;
                this.state.affiliatetotalLiveDnmc = affiliatetotalLiveDnmc;
                this.state.affiliatetotalPortalDnmc = affiliatetotalPortalDnmc;
                this.state.affiliatetotalCrmDnmc = affiliatetotalCrmDnmc;
                this.state.affiliatetotalCrmDnmcPer = affiliatetotalCrmDnmcPer;
                this.state.affiliatetotalLiveWorkable = affiliatetotalLiveWorkable;
                this.state.affiliatetotalPortalWorkable = affiliatetotalPortalWorkable;
                this.state.affiliatetotalCrmWorkable = affiliatetotalCrmWorkable;
                this.state.affiliatetotalCrmWorkablePer = affiliatetotalCrmWorkablePer;
                this.state.affiliatetotalLiveDeclinedLead = affiliatetotalLiveDeclinedLead;
                this.state.affiliatetotalPortalDeclinedLead = affiliatetotalPortalDeclinedLead;
                this.state.affiliatetotalCrmDeclinedLead = affiliatetotalCrmDeclinedLead;
                this.state.affiliatetotalCrmDeclinedLeadPer = affiliatetotalCrmDeclinedLeadPer;
                this.state.affiliatetotalLiveDncLead = affiliatetotalLiveDncLead;
                this.state.affiliatetotalPortalDncLead = affiliatetotalPortalDncLead;
                this.state.affiliatetotalCrmDncLead = affiliatetotalCrmDncLead;
                this.state.affiliatetotalCrmDncLeadPer = affiliatetotalCrmDncLeadPer;
                this.state.affiliatetotalLiveTransferredLead = affiliatetotalLiveTransferredLead;
                this.state.affiliatetotalPortalTransferredLead = affiliatetotalPortalTransferredLead;
                this.state.affiliatetotalCrmTransferredLead = affiliatetotalCrmTransferredLead;
                this.state.affiliatetotalCrmTransferredLeadPer = affiliatetotalCrmTransferredLeadPer;
                this.state.affiliatetotalLiveNoContactLead = affiliatetotalLiveNoContactLead;
                this.state.affiliatetotalPortalNoContactLead = affiliatetotalPortalNoContactLead;
                this.state.affiliatetotalCrmNoContactLead = affiliatetotalCrmNoContactLead;
                this.state.affiliatetotalCrmNoContactLeadPer = affiliatetotalCrmNoContactLeadPer;
                this.state.affiliatetotalLiveNoResponseLead = affiliatetotalLiveNoResponseLead;
                this.state.affiliatetotalPortalNoResponseLead = affiliatetotalPortalNoResponseLead;
                this.state.affiliatetotalCrmNoResponseLead = affiliatetotalCrmNoResponseLead;
                this.state.affiliatetotalCrmNoResponseLeadPer = affiliatetotalCrmNoResponseLeadPer;
                this.state.affiliatetotalPrimeLead = affiliatetotalPrimeLead;
                this.state.affiliatetotalSubPrimeLead = affiliatetotalSubPrimeLead;
                this.state.affiliatetotalPrimeDupLead = affiliatetotalPrimeDupLead;
                this.state.affiliatetotalSubPrimeDupLead = affiliatetotalSubPrimeDupLead;
                this.state.affiliatetotalPrimeDnmcLead = affiliatetotalPrimeDnmcLead;
                this.state.affiliatetotalSubPrimeDnmcLead = affiliatetotalSubPrimeDnmcLead;
                this.state.affiliatetotalPrimeWorkableLead = affiliatetotalPrimeWorkableLead;
                this.state.affiliatetotalSubPrimeWorkableLead = affiliatetotalSubPrimeWorkableLead;
                this.state.affiliatetotalPrimeDeclinedLead = affiliatetotalPrimeDeclinedLead;
                this.state.affiliatetotalSubPrimeDeclinedLead = affiliatetotalSubPrimeDeclinedLead;
                this.state.affiliatetotalPrimeDncLead = affiliatetotalPrimeDncLead;
                this.state.affiliatetotalSubPrimeDncLead = affiliatetotalSubPrimeDncLead;
                this.state.affiliatetotalPrimeTransferredLead = affiliatetotalPrimeTransferredLead;
                this.state.affiliatetotalSubPrimeTransferredLead = affiliatetotalSubPrimeTransferredLead;
                this.state.affiliatetotalPrimeNoContactLead = affiliatetotalPrimeNoContactLead;
                this.state.affiliatetotalSubPrimeNoContactLead = affiliatetotalSubPrimeNoContactLead;
                this.state.affiliatetotalPrimeNoResponseLead = affiliatetotalPrimeNoResponseLead;
                this.state.affiliatetotalSubPrimeNoResponseLead = affiliatetotalSubPrimeNoResponseLead;
                
                
            }
            console.log(return_data)
            // return return_data;
            
            
        } catch (error) {
            console.error("Error fetching New Crm leads:", error);
        }
    }
                                        // Affiliate Sales Dashboard Starting

    
}

OdooCRMDashboard.template = "owl.OdooCRMDashboard";
registry.category("actions").add("OdooCRMDashboard", OdooCRMDashboard);


