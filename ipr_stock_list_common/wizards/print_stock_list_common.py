# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from openerp import api, models, fields
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class StockPrintListCommon(models.AbstractModel):
    _name = "stock.print_list_common"
    _description = "Print List Common"

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
        relation="rel_print_list_2_warehouse",
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
        raise UserError(
            _("This feature hasn't been implemented yet"))

    @api.multi
    def action_print_ods(self):
        raise UserError(
            _("This feature hasn't been implemented yet"))

    @api.multi
    def action_print_sreen(self):
        raise UserError(
            _("This feature hasn't been implemented yet"))

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
