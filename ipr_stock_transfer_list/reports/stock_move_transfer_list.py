# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockMoveTransferList(models.Model):
    _name = "stock.move_transfer_list"
    _inherit = "stock.move_list_common"
    _auto = False

    source_loc_wh_id = fields.Many2one(
        string="Warehouse Source Location",
        comodel_name="stock.warehouse",
    )

    source_dest_loc_wh_id = fields.Many2one(
        string="Warehouse Dest. Location",
        comodel_name="stock.warehouse",
    )

    def _select_field(self):
        _super = super(StockMoveTransferList, self)
        new_query = """
            C.warehouse_id AS source_loc_wh_id,
            E.warehouse_id AS source_dest_loc_wh_id
        """
        select_field_str = (
            _super._select_field() +
            "," +
            new_query
        )
        return select_field_str

    def _join(self):
        _super = super(StockMoveTransferList, self)
        new_query = """
            JOIN stock_move AS D ON A.move_dest_id=D.id
            JOIN stock_picking_type AS E ON D.picking_type_id=E.id
        """
        join_str = (
            _super._join() +
            new_query
        )
        return join_str

    def _get_subtype(self, cr):
        query = """
            SELECT  res_id
            FROM    ir_model_data
            WHERE   module = 'stock_interwarehouse_operation'
            AND     name = 'inter_warehouse_out_subtype'
        """
        cr.execute(query)
        subtype_id = cr.fetchone()[0]
        return subtype_id
