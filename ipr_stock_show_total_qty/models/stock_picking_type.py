# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    qty_ok = fields.Boolean(
        string="Show Total Qty",
        default=False,
    )
