# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields


class PosOrderExportAccurate(models.TransientModel):
    _name = "pos.order_export_accurate"

    description = fields.Text(
        string="Description"
    )
    accurate_invoice_no = fields.Char(
        string="Accurate(INVOICENO)",
        required=True
    )
    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        required=True
    )
    date = fields.Date(
        string="Date",
        required=True
    )

    @api.multi
    def action_print_xml(self):
        datas = {}
        datas['form'] = self.read()[0]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': "aeroo_reportPosOrderAccurate",
            'datas': datas,
        }
