# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields


class PrintStockTransferInList(models.TransientModel):
    _name = "stock.print_transfer_in_list"
    _inherit = ["stock.print_list_common"]

    warehouse_ids = fields.Many2many(
        string="Warehouse(s)",
        comodel_name="stock.warehouse",
        relation="rel_stock_trans_in_list_2_warehouse",
        column1="wizard_id",
        column2="warehouse_id",
        required=True,
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Transfer In Products",
        comodel_name="product.product",
        related="company_id.allowed_transfer_in_product_ids",
        store=False,
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Transfer In Product Categories",
        comodel_name="product.category",
        related="company_id.allowed_transfer_in_product_categ_ids",
        store=False,
    )
    product_ids = fields.Many2many(
        string="Product(s)",
        comodel_name="product.product",
        relation="rel_stock_trans_in_list_2_product",
        column1="wizard_id",
        column2="product_id",
    )

    @api.multi
    def action_print_xls(self):
        datas = {}
        datas["form"] = self.read()[0]
        return {
            "type": "ir.actions.report.xml",
            "report_name": "stock_transfer_in_list_xls",
            "datas": datas,
        }

    @api.multi
    def action_print_ods(self):
        datas = {}
        datas["form"] = self.read()[0]
        return {
            "type": "ir.actions.report.xml",
            "report_name": "stock_transfer_in_list_ods",
            "datas": datas,
        }

    @api.multi
    def action_print_sreen(self):
        waction = self.env.ref(
            "ipr_stock_transfer_in_list."
            "stock_move_transfer_in_list_action")
        context = {}
        domain = [
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
            ("picking_type_id.warehouse_id", "in", self.warehouse_ids.ids),
        ]
        if self.product_ids:
            domain += [
                ("product_id", "in", self.product_ids.ids)
            ]
        result = waction.read()[0]
        result.update({"context": context, "domain": domain})
        return result
