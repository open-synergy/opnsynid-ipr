# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockMoveWasteList(models.Model):
    _name = "stock.move_waste_list"
    _inherit = "stock.move_list_common"
    _auto = False

    def _get_subtype(self, cr):
        query = """
            SELECT  res_id
            FROM    ir_model_data
            WHERE   module = 'stock_waste_operation'
            AND     name = 'waste_subtype'
        """
        cr.execute(query)
        subtype_id = cr.fetchone()[0]
        return subtype_id
