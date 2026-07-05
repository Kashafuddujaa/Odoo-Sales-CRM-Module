/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class SalesCrmDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ loading: true, data: null });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        this.state.loading = true;
        this.state.data = await this.orm.call(
            "sales.crm.dashboard",
            "get_dashboard_data",
            []
        );
        this.state.loading = false;
    }

    formatCurrency(value) {
        const symbol = this.state.data ? this.state.data.currency_symbol : "";
        const amount = Number(value || 0).toLocaleString(undefined, {
            minimumFractionDigits: 0,
            maximumFractionDigits: 0,
        });
        return `${symbol}${amount}`;
    }

    get maxStageValue() {
        const stages = this.state.data ? this.state.data.by_stage : [];
        return stages.reduce((max, s) => Math.max(max, s.value), 0) || 1;
    }

    stageWidth(value) {
        return `${Math.round((value / this.maxStageValue) * 100)}%`;
    }

    openPipeline() {
        this.action.doAction("sales_crm.action_sales_crm_pipeline");
    }

    openOverdue() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Overdue Follow-ups",
            res_model: "sales.crm.followup",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: [["is_overdue", "=", true]],
        });
    }
}

SalesCrmDashboard.template = "sales_crm.Dashboard";

registry.category("actions").add("sales_crm_dashboard", SalesCrmDashboard);
