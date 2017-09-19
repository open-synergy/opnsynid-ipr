# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, SUPERUSER_ID
import openerp.addons.decimal_precision as dp


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    @api.depends(
        "state",
        "picking_type_id.qty_ok"
    )
    def _compute_qty_policy(self):
        user_id = self.env.user.id
        for picking in self:
            if user_id == SUPERUSER_ID:
                picking.show_qty = True
                continue

            if picking.picking_type_id.qty_ok:
                picking.show_qty = True
            else:
                picking.show_qty = False

    show_qty = fields.Boolean(
        string="Show Qty",
        compute="_compute_qty_policy",
        store=False,
    )

    total_qty = fields.Float(
        compute='_compute_total_qty',
        string="Total Qty",
        digits=dp.get_precision('Product Unit of Measure')
    )

    @api.depends(
        'move_lines', 'move_lines.product_uom_qty')
    def _compute_total_qty(self):
        for picking in self:
            total_qty = sum(picking.move_lines.mapped('product_uom_qty'))
            picking.total_qty = total_qty
