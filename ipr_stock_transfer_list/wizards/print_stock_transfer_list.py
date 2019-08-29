# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields


class PrintStockTransferList(models.TransientModel):
    _name = "stock.print_transfer_list"
    _inherit = ["stock.print_list_common"]

    warehouse_ids = fields.Many2many(
        string="Warehouse(s)",
        comodel_name="stock.warehouse",
        relation="rel_stock_trans_list_2_warehouse",
        column1="wizard_id",
        column2="warehouse_id",
        required=True,
    )

    @api.multi
    def action_print_xls(self):
        datas = {}
        datas["form"] = self.read()[0]
        return {
            "type": "ir.actions.report.xml",
            "report_name": "stock_transfer_list_xls",
            "datas": datas,
        }

    @api.multi
    def action_print_ods(self):
        datas = {}
        datas["form"] = self.read()[0]
        return {
            "type": "ir.actions.report.xml",
            "report_name": "stock_transfer_list_ods",
            "datas": datas,
        }

    @api.multi
    def action_print_sreen(self):
        waction = self.env.ref(
            "ipr_stock_transfer_list."
            "stock_move_transfer_list_action")
        context = {}
        domain = [
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
            ("picking_type_id.warehouse_id", "in", self.warehouse_ids.ids),
        ]
        result = waction.read()[0]
        result.update({"context": context, "domain": domain})
        return result
