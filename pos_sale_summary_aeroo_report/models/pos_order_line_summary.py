# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp.tools import drop_view_if_exists


class PosOrderLineSummary(models.Model):
    _name = "pos.order_line_summary"
    _description = "PoS Order Line Summary"
    _auto = False

    date_order = fields.Datetime(
        string="Order Date"
    )
    config_id = fields.Many2one(
        string="Config",
        comodel_name="pos.config",
    )
    pos_categ_id = fields.Many2one(
        string="Product Category",
        comodel_name="pos.category",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    qty = fields.Float(
        string="Qty",
    )
    price_subtotal = fields.Float(
        string="Subtotal",
    )

    def _select(self):
        select_str = """
            SELECT
                row_number() OVER() AS id,
                B.date_order,
                C.config_id,
                D.pos_categ_id AS pos_categ_id,
                A.product_id AS product_id,
                SUM(A.qty) AS qty,
                SUM(A.price_subtotal) AS price_subtotal
        """
        return select_str

    def _from(self):
        from_str = """
            FROM pos_order_line AS A
            JOIN pos_order AS B ON A.order_id=B.id
            JOIN pos_session AS C ON B.session_id=C.id
            JOIN product_template AS D ON A.product_id=D.id
            WHERE D.pos_categ_id IS NOT NULL AND
                  B.state NOT IN ('draft', 'cancel')
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY 2,3,4,5
            ORDER BY pos_categ_id
        """
        return group_by_str

    def init(self, cr):
        drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            %s
            %s
            )""" % (
            self._table,
            self._select(),
            self._from(),
            self._group_by()
        ))
