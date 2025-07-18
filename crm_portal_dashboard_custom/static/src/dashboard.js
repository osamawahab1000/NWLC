// /** @odoo-module */
// import { registry} from '@web/core/registry';
// import { useService } from "@web/core/utils/hooks";
// const { Component, onWillStart, onMounted} = owl
// import { jsonrpc } from "@web/core/network/rpc_service";
// import { _t } from "@web/core/l10n/translation";
// import { session } from "@web/session";
// import { WebClient } from "@web/webclient/webclient";
// export class CRMDashboard extends Component {
//     setup() {
//         this.action = useService("action");
//         this.orm = useService("orm");
//         onWillStart(this.onWillStart);
//         onMounted(this.onMounted);
//     }


//     on_change_income_expense_values(e) {
//         e.stopPropagation();
//         var $target = $(e.target);
//         var value = $target.val();
//         if (value == "this_year") {
//             this.onclick_this_year($target.val());
//         } else if (value == "this_quarter") {
//             this.onclick_this_quarter($target.val());
//         } else if (value == "this_month") {
//             this.onclick_this_month($target.val());
//         } else if (value == "this_week") {
//             this.onclick_this_week($target.val());
//         }
//     }


//     onclick_this_week(ev) {
//         var self = this;
//         jsonrpc('/web/dataset/call_kw/crm.lead/crm_week', {
//                 model: 'crm.lead',
//                 method: 'crm_week',
//                 args: [{}],
//                 kwargs: {},
//             })
//     }
//     onclick_this_year(ev) {
//         var self = this;
//         jsonrpc('/web/dataset/call_kw/crm.lead/crm_week', {
//                 model: 'crm.lead',
//                 method: 'crm_week',
//                 args: [{}],
//                 kwargs: {},
//             })
//     }
//     onclick_this_quarter(ev) {
//         var self = this;
//         jsonrpc('/web/dataset/call_kw/crm.lead/crm_week', {
//                 model: 'crm.lead',
//                 method: 'crm_week',
//                 args: [{}],
//                 kwargs: {},
//             })
//     }
//     onclick_this_month(ev) {
//         var self = this;
//         jsonrpc('/web/dataset/call_kw/crm.lead/crm_week', {
//                 model: 'crm.lead',
//                 method: 'crm_week',
//                 args: [{}],
//                 kwargs: {},
//             })
//     }
// }
    