# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp.tools import drop_view_if_exists


class StockMoveListCommon(models.AbstractModel):
    _name = "stock.move_list_common"
    _description = "Stock Move List Common"
    _auto = False

    move_id = fields.Many2one(
        string="Move",
        comodel_name="stock.move",
    )
    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
    )
    date = fields.Datetime(
        string="Date",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
    )
    picking_id = fields.Many2one(
        string="Internal Reference",
        comodel_name="stock.picking",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    product_qty = fields.Float(
        string="Product Qty",
    )
    product_uom_id = fields.Many2one(
        string="Product UoM",
        comodel_name="product.uom",
    )
    source_loc_id = fields.Many2one(
        string="Source Location",
        comodel_name="stock.location",
    )
    dest_loc_id = fields.Many2one(
        string="Destination Location",
        comodel_name="stock.location",
    )
    picking_type_id = fields.Many2one(
        string="Picking Type",
        comodel_name="stock.picking.type",
    )

    def _get_subtype(self, cr):
        return False

    def _select(self, order_by):
        select_str = """
            SELECT
                row_number() OVER(%s) as id
        """ % (order_by)
        select_str = (
            select_str +
            "," +
            self._select_field()
        )
        return select_str

    def _select_field(self):
        select_field_str = """
                A.id as move_id,
                A.warehouse_id AS warehouse_id,
                A.company_id AS company_id,
                A.date AS date,
                B.partner_id AS partner_id,
                A.picking_id AS picking_id,
                A.product_id AS product_id,
                A.product_qty AS product_qty,
                A.location_id AS source_loc_id,
                A.location_dest_id AS dest_loc_id,
                e.uom_id AS product_uom_id,
                B.picking_type_id AS picking_type_id
        """
        return select_field_str

    def _from(self):
        from_str = """
            FROM stock_move AS A
        """
        return from_str

    def _join(self):
        join_str = """
            JOIN stock_picking AS B ON A.picking_id=B.id
            JOIN stock_picking_type AS C ON B.picking_type_id=C.id
            JOIN product_product AS x ON A.product_id = x.id
            JOIN product_template AS y ON x.product_tmpl_id = y.id
        """
        return join_str

    def _where(self, subtype_id):
        where_str = """
            WHERE A.state='done'
        """
        if subtype_id:
            where_str = where_str + """
                AND C.subtype_id=%s
            """ % (subtype_id)
        return where_str

    def _order_by(self):
        join_str = """
            ORDER BY A.date, A.id
        """
        return join_str

    def init(self, cr):
        drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        subtype_id = self._get_subtype(cr)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            %s
            %s
            %s
            %s
        )""" % (
            self._table,
            self._select(self._order_by()),
            self._from(),
            self._join(),
            self._where(subtype_id),
            self._order_by(),
        ))
