    # -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from openerp import api, models, fields


class PrintPosSaleSummary(models.TransientModel):
    _name = "stock.print_pos_sale_summary"
    _description = "Print PoS Sales Summary"

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
        relation="pos_config_sale_summary_rel",
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
            "report_name": "pos_sale_summary_pdf",
            "datas": datas,
        }
