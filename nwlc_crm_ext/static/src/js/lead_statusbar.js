/** @odoo-module **/

import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { StatusBarField } from "@web/views/fields/statusbar/statusbar_field";
import { useService } from "@web/core/utils/hooks";
import { formatDuration } from "@web/core/l10n/dates";
import { Dialog } from "@web/core/dialog/dialog";




patch(StatusBarField.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.notification = useService("notification");
    },

    async selectItem(item) {
        const resModel = this.props.record.model.env.searchModel.resModel;
        const record = this.props.record.data;
        const stageValue = item.value;
        const leadId = this.props.record.evalContext.id;
        const isLead = resModel === "crm.lead" && record.type === "lead";
        const isOpportunity = resModel === "crm.lead" && record.type === "opportunity";

        // For Opportunity DEAD stage
        if (isOpportunity && stageValue === 13) {
            // Check if processing_owner is set (should not be empty)
            if (!record.processing_owner || !record.processing_owner[0]){
                this.env.services.notification.add("Please Select an Owner first!",{
                    type:"danger",
                    sticky:false,
                });
                return;
            }

            try {
                console.log("Calling backend restriction check...");
                await this.orm.call("crm.lead", "check_dead_stage_restriction_js", [[leadId]]);
                console.log("Backend check passed!");

                // Show reason wizard
                await this.actionService.doAction({
                    type: 'ir.actions.act_window',
                    res_model: 'dead.reason.wizard',
                    views: [[false, 'form']],
                    view_mode: "form",
                    name: 'Processing Stage',
                    context: {
                        default_lead_id: leadId,
                        default_next_stage_id: stageValue,  // pass new stage
                    },
                    target: 'new',
                });
            } catch (error) {
                console.error("Backend error:", error);
                this.notification.add("You cannot set this record to 'Dead' while it has a lender with 'Approved Personal' status!", {
                    type: "danger",
                });
            }

            return; // Stop further execution for Dead stage
        
        }

        //  For Lead DEAD stage
        if (isLead && stageValue === 5) {
            // Check if processing_owner is set (should not be empty)
            // if (!record.processing_owner || !record.processing_owner[0]){
            //     this.env.services.notification.add("Please Select an Owner first!",{
            //         type:"danger",
            //         sticky:false,
            //     });
            //     return;
            // }

            try {
                // console.log("Calling backend restriction check...");
                // await this.orm.call("crm.lead", "check_dead_stage_restriction_js", [[leadId]]);
                // await this.orm.call("crm.lead", [[leadId]]);
                console.log(" Backend check passed!");

                // Show reason wizard
                await this.actionService.doAction({
                    type: 'ir.actions.act_window',
                    res_model: 'dead.reason.wizard',
                    views: [[false, 'form']],
                    view_mode: "form",
                    name: 'Lead Stage',
                    context: {
                        default_lead_id: leadId,
                        default_next_stage_id: stageValue,
                    },
                    target: 'new',
                });
            } catch (error) {
                console.error(" Backend error:", error);
                // this.notification.add("You cannot set this record to 'Dead' while it has a lender with 'Approved Personal' status!", {
                //     type: "danger",
                // });
            }

            return; // Stop further execution for Dead stage
        
        }

        // For non-dead stage with reason
        if (
            (isLead && ![5, 7, 9].includes(stageValue)) ||
            record.type === "opportunity"
        ) {
            await this.actionService.doAction({
                type: 'ir.actions.act_window',
                res_model: 'stage.wizard',
                views: [[false, 'form']],
                view_mode: "form",
                name: 'Lead Stage',
                context: {
                    default_lead_id: leadId,
                    default_next_stage_id: stageValue,  // pass new stage
                },
                target: 'new',
            });

            // Don’t change stage until wizard applies
            return;
        }

        //  fallback for untouched stages (if any)
        await super.selectItem(item);
    }
});














// patch(StatusBarField.prototype, {
//     setup() {
//         super.setup(...arguments);
//         this.orm = useService("orm");
//         this.actionService = useService("action");
//     },

//     async selectItem(item) {
//         console.log(item)

//         if (this.props.record.model.env.searchModel.resModel === "crm.lead" && (this.props.record.data.type === "lead" && [5].includes(item.value))){

//             if (!this.props.record.data.user_id || !this.props.record.data.user_id[0]){
//                 this.env.services.notification.add("Please Select an Owner first!",{
//                     type:"danger",
//                     sticky:false,
//                 });
//                 return;
//             }
//             // else (
//             this.actionService.doAction({                
//                 type: 'ir.actions.act_window',
//                 res_model: 'dead.reason.wizard',
//                 views: [[false, 'form']],
//                 view_mode: "form",
//                 name: 'Lead Stage',
//                 context: {'default_lead_id': this.props.record.evalContext.id},
//                 target: 'new',               
//             });
//         }
        
//         super.selectItem(item);
//         if (this.props.record.model.env.searchModel.resModel === "crm.lead" && (this.props.record.data.type === "lead" && ![5,7,9].includes(item.value)) || (this.props.record.data.type === "opportunity")) { 
//             this.actionService.doAction({                
//                 type: 'ir.actions.act_window',
//                 res_model: 'stage.wizard',
//                 views: [[false, 'form']],
//                 view_mode: "form",
//                 name: 'Lead Stage',
//                 context: {'default_lead_id': this.props.record.evalContext.id},
//                 target: 'new',               
//             });
//         }
//     },

    
// });

// patch(Dialog.prototype, {
//     setup() {
//         super.setup(...arguments);
//         if (this.props?.body && typeof this.props.body === "string") {
//             if (this.props.body.includes("You cannot set this record to 'Dead' while it has a lender with 'Approved Personal' status.")) {
//                 const originalClose = this.close;
//                 this.close = (...args) => {
//                     this.env.services.action.reload(); // 🔁 Refresh view
//                     return originalClose.call(this, ...args);
//                 };
//             }
//         }
//     },
// });






