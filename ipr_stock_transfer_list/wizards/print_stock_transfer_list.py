# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from openerp import api, models, fields
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class PrintStockTransferList(models.TransientModel):
    _name = "stock.print_transfer_list"
    _description = "Print Transfer List"

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.user.company_id.id,
    )
    date_start = fields.Datetime(
        string="Date Start",
    )
    date_end = fields.Datetime(
        string="Date End",
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    warehouse_ids = fields.Many2many(
        string="Warehouse(s)",
        comodel_name="stock.warehouse",
        relation="rel_stock_trans_list_2_warehouse",
        column1="wizard_id",
        column2="warehouse_id",
        required=True,
    )
    output_format = fields.Selection(
        string="Output Format",
        required=True,
        selection=[
            ("screen", "On-Screen"),
            ("xls", "XLS"),
            ("ods", "ODS")
        ],
        default="ods",
    )

    @api.constrains(
        "date_start", "date_end")
    def _check_date(self):
        strWarning = _(
            "Date start must be greater than date end")
        if self.date_start and self.date_end:
            if self.date_start > self.date_end:
                raise UserError(strWarning)

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
        criteria = [
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
            ("picking_type_id.warehouse_id", "in", self.warehouse_ids.ids),
        ]
        waction.domain = criteria
        return waction.read()[0]

    @api.multi
    def action_print(self):
        self.ensure_one()

        if self.output_format == "screen":
            result = self.action_print_sreen()
        elif self.output_format == "ods":
            result = self.action_print_ods()
        elif self.output_format == "xls":
            result = self.action_print_xls()
        else:
            raise UserError(_("No Output Format Selected"))

        return result
