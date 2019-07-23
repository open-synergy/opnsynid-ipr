# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.tools import drop_view_if_exists


class StockMoveTransferList(models.Model):
    _name = "stock.move_transfer_list"
    _description = "Stock Move Transfer List"
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

    @api.depends("source_loc_id")
    @api.multi
    def _compute_source_loc_wh_id(self):
        obj_stock_location = self.env["stock.location"]
        for rec in self:
            loc_wh_id = obj_stock_location.get_warehouse(rec.source_loc_id)
            rec.source_loc_wh_id = loc_wh_id

    source_loc_wh_id = fields.Many2one(
        string="Warehouse Source Location",
        comodel_name="stock.warehouse",
        compute="_compute_source_loc_wh_id",
    )
    dest_loc_id = fields.Many2one(
        string="Destination Location",
        comodel_name="stock.location",
    )

    @api.depends("dest_loc_id")
    @api.multi
    def _compute_source_dest_loc_wh_id(self):
        obj_stock_location = self.env["stock.location"]
        for rec in self:
            dest_loc_wh_id = obj_stock_location.get_warehouse(rec.dest_loc_id)
            rec.source_dest_loc_wh_id = dest_loc_wh_id

    source_dest_loc_wh_id = fields.Many2one(
        string="Warehouse Dest. Location",
        comodel_name="stock.warehouse",
        compute="_compute_source_dest_loc_wh_id",
    )
    picking_type_id = fields.Many2one(
        string="Picking Type",
        comodel_name="stock.picking.type",
    )

    def _get_subtype(self):
        return self.env.ref(
            "stock_interwarehouse_operation"
            ".inter_warehouse_out_subtype"
        )

    def _select(self):
        select_str = """
            SELECT
                row_number() OVER() as id,
                A.id as move_id,
                A.warehouse_id AS warehouse_id,
                A.company_id AS company_id,
                A.date AS date,
                A.picking_id AS picking_id,
                A.product_id AS product_id,
                A.product_qty AS product_qty,
                A.location_id AS source_loc_id,
                A.location_dest_id AS dest_loc_id,
                A.product_uom AS product_uom_id,
                B.picking_type_id AS picking_type_id
        """
        return select_str

    def _from(self):
        from_str = """
            FROM stock_move AS A
        """
        return from_str

    def _join(self):
        join_str = """
            JOIN stock_picking AS B ON A.picking_id=B.id
            JOIN stock_picking_type AS C ON B.picking_type_id=C.id
        """
        return join_str

    def _where(self, subtype_id):
        where_str = """
            WHERE A.state='done' AND
                  C.subtype_id=%s
        """ % (subtype_id)
        return where_str

    def init(self, cr):
        drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        query = """
            SELECT  res_id
            FROM    ir_model_data
            WHERE   module = 'stock_interwarehouse_operation'
            AND     name = 'inter_warehouse_out_subtype'
        """
        cr.execute(query)
        subtype_id = cr.fetchone()[0]

        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            %s
            %s
            %s
        )""" % (
            self._table,
            self._select(),
            self._from(),
            self._join(),
            self._where(subtype_id)
        ))
