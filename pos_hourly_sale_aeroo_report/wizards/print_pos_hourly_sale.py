    # -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from openerp import api, models, fields
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class PrintHourlySale(models.TransientModel):
    _name = "stock.print_hourly_sale"
    _description = "Print PoS Hourly Sales"

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.user.company_id.id,
    )
    date = fields.Date(
        string="Date",
        default=datetime.now().strftime("%Y-%m-%d"),
    )
    config_ids = fields.Many2many(
        string="Point Of Sale",
        comodel_name="pos.config",
        relation="pos_config_hourly_sale_rel",
        column1="wizard_id",
        column2="config_id"
    )

    @api.multi
    def action_print(self):
        self.ensure_one()

        datas = {}

        datas['form'] = self.read()[0]

        return {
            "type": "ir.actions.report.xml",
            "report_name": "hourly_sale_pdf",
            "datas": datas,
        }