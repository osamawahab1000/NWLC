/** @odoo-module **/

import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { useHotkey } from "@web/core/hotkeys/hotkey_hook";
import { registry } from "@web/core/registry";
import { useSortable } from "@web/core/utils/sortable_owl";
import { isNull } from "@web/views/utils";
import { ColumnProgress } from "@web/views/view_components/column_progress";
import { useBounceButton } from "@web/views/view_hook";
import { Component, onWillStart, onWillUpdateProps } from "@odoo/owl";

patch(KanbanRenderer.prototype, {


    setup() {
        super.setup();

        this.companyService = useService("company");
    },

    /**
     * Override the getGroupsOrRecords function to customize its behavior.
     */
    getGroupsOrRecords() {
        
        const { list } = this.props;
        if (list.isGrouped) {
            var GroupRecords = [...list.groups]
                .sort((a, b) => (a.value && !b.value ? 1 : !a.value && b.value ? -1 : 0))
                .map((group, i) => ({
                    group,
                    key: isNull(group.value) ? `group_key_${i}` : String(group.value),
                }));
            if (this.props.list.config.resModel === "crm.lead"){
                if (this.props.list.config.groupBy[0] === 'stage_id'){
                    var currentCompanyId = this.companyService.currentCompany.id;
                    var stage_company_ids = this.props.list.model.crm_stages;
                    
                    var filteredGroupRecords = GroupRecords.filter((c_group) => {
                        return stage_company_ids[c_group.key] === currentCompanyId;
                    });
                    return filteredGroupRecords;
                }
                if (this.props.list.config.groupBy[0] === 'lead_stage_id'){
                    return GroupRecords;
                }
            } else {
                return GroupRecords;
            }


        } else {
            return list.records.map((record) => ({ record, key: record.id }));
        }
        
    },
});
