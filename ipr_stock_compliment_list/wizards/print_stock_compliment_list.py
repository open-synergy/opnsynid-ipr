# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields, _
from openerp.exceptions import Warning as UserError


class PrintStockComplimentList(models.TransientModel):
    _name = "stock.print_compliment_list"
    _inherit = ["stock.print_list_common"]

    warehouse_ids = fields.Many2many(
        string="Warehouse(s)",
        comodel_name="stock.warehouse",
        relation="rel_stock_compliment_list_2_warehouse",
        column1="wizard_id",
        column2="warehouse_id",
        required=True,
    )

    allowed_product_ids = fields.Many2many(
        string="Allowed Compliment Products",
        comodel_name="product.product",
        related="company_id.allowed_compliment_product_ids",
        store=False,
    )

    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Compliment Product Categories",
        comodel_name="product.category",
        related="company_id.allowed_compliment_product_categ_ids",
        store=False,
    )

    product_ids = fields.Many2many(
        string="Product(s)",
        comodel_name="product.product",
        relation="rel_stock_compliment_list_2_product",
        column1="wizard_id",
        column2="product_id",
    )

    @api.multi
    def action_print_xls(self):
        datas = {}
        datas["form"] = self.read()[0]
        return {
            "type": "ir.actions.report.xml",
            "report_name": "stock_compliment_list_xls",
            "datas": datas,
        }

    @api.multi
    def action_print_ods(self):
        datas = {}
        datas["form"] = self.read()[0]
        return {
            "type": "ir.actions.report.xml",
            "report_name": "stock_compliment_list_ods",
            "datas": datas,
        }

    @api.multi
    def action_print_sreen(self):
        waction = self.env.ref(
            "ipr_stock_compliment_list."
            "stock_move_compliment_list_action")
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
