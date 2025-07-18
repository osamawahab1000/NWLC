/** @odoo-module */

import { useSubEnv } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import {
  deleteConfirmationMessage,
  ConfirmationDialog,
} from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { CogMenu } from "@web/search/cog_menu/cog_menu";
import { evaluateBooleanExpr } from "@web/core/py_js/py";
import { Layout } from "@web/search/layout";
import { usePager } from "@web/search/pager_hook";
import { SearchBar } from "@web/search/search_bar/search_bar";
import { useSearchBarToggler } from "@web/search/search_bar/search_bar_toggler";
import { session } from "@web/session";
import { useSetupView } from "@web/views/view_hook";
import { useModelWithSampleData } from "@web/model/model";
import { standardViewProps } from "@web/views/standard_view_props";
import { MultiRecordViewButton } from "@web/views/view_button/multi_record_view_button";
import { useViewButtons } from "@web/views/view_button/view_button_hook";
import {
  addFieldDependencies,
  extractFieldsFromArchInfo,
} from "@web/model/relational_model/utils";
import { registry } from "@web/core/registry";

import { Component, reactive, useRef, useState } from "@odoo/owl";

const QUICK_CREATE_FIELD_TYPES = [
  "char",
  "boolean",
  "many2one",
  "selection",
  "many2many",
];

//export class CrmStagesKanbanController extends KanbanController {
patch(KanbanController.prototype, {
  setup() {
    super.setup();
    this.companyService = useService("company");
    this.actionService = useService("action");
    this.dialog = useService("dialog");
    const { Model, archInfo } = this.props;

    class KanbanSampleModel extends Model {
      setup() {
        super.setup(...arguments);
        this.initialSampleGroups = undefined;
        this.crm_stages = false;
      }

      /**
       * @override
       */
      hasData() {
        if (this.root.groups) {
          if (!this.root.groups.length) {
            // While we don't have any data, we want to display the column quick create and
            // example background. Return true so that we don't get sample data instead
            return true;
          }
          return this.root.groups.some((group) => group.hasData);
        }

        return super.hasData();
      }

      async load() {

        console.log('load', this.props)
        console.log('load', window.location.href.includes("action-210"))
        console.log('load' ,window.location)
        if (this.orm.isSample && this.initialSampleGroups) {
          this.orm.setGroups(this.initialSampleGroups);
        }
        return super.load(...arguments);
      }

      async _webReadGroup() {
        const result = await super._webReadGroup(...arguments);       
          if (!this.crm_stages) {
            if (this.config.resModel === "crm.lead") {
              var stage_company_ids = await this.orm.call(
                "crm.stage",
                "get_stages_company",
                [],
                {}
              );

              this.crm_stages = stage_company_ids;
            }
          }
          if (!this.initialSampleGroups) {
            this.initialSampleGroups = JSON.parse(
              JSON.stringify(result.groups)
            );
          }
        return result;
      }

      removeSampleDataInGroups() {
        if (this.useSampleModel) {
          for (const group of this.root.groups) {
            const list = group.list;
            console.log("removeSampleDataInGroups" + list.records);
            group.count = 0;
            list.count = 0;
            if (list.records) {
              list.records = [];
            } else {
              list.groups = [];
            }
          }
        }
      }
    }

    this.model = useState(
      useModelWithSampleData(
        KanbanSampleModel,
        this.modelParams,
        this.modelOptions
      )
    );
  },

  async createRecord() {
    console.log('create',window.location)
    if (window.location.href.includes("action-210")){

      const { onCreate } = this.props.archInfo;
        const { root } = this.model;
        if (this.canQuickCreate && onCreate === "quick_create") {
            const firstGroup = root.groups[0];
            if (firstGroup.isFolded) {
                await firstGroup.toggle();
            }
            this.quickCreateState.groupId = firstGroup.id;
        } else if (onCreate && onCreate !== "quick_create") {
            const options = {
                additionalContext: root.context,
                onClose: async () => {
                    await root.load();
                    this.model.useSampleModel = false;
                    this.render(true); // FIXME WOWL reactivity
                },
            };
            await this.actionService.doAction(onCreate, options);
        } else {
            await this.props.createRecord();
        }
    }else{

     
      if (!this.model.crm_stages) {
        return super.createRecord();
      }
      const { onCreate } = this.props.archInfo;
      const { root } = this.model;
      if (this.canQuickCreate && onCreate === "quick_create") {
        var currentCompanyId = this.companyService.currentCompany.id;
        var filteredGroupRecords = root.groups.filter((c_group) => {
          return (
            this.model.crm_stages[c_group.serverValue] === currentCompanyId
          );
        });
        const firstGroup = filteredGroupRecords[0];
        if (firstGroup.isFolded) {
          await firstGroup.toggle();
        }
        this.quickCreateState.groupId = firstGroup.id;
      } else if (onCreate && onCreate !== "quick_create") {
        const options = {
          additionalContext: root.context,
          onClose: async () => {
            await root.load();
            this.model.useSampleModel = false;
            this.render(true); // FIXME WOWL reactivity
          },
        };
        await this.actionService.doAction(onCreate, options);
      } else {
        await this.props.createRecord();
      }
    }
  },
});

async function _mockGetStagesCompanies(params) {
  /* Mock function for when there aren't records to be shown. */
  return {};
}

registry
  .category("sample_server")
  .add("get_stages_company", _mockGetStagesCompanies);

registry.category("sample_server").add("res.partner/some_method", () => 23);
