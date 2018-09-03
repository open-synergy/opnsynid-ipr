# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    accurate_dept_id = fields.Char(
        string="DEPTID"
    )
    accurate_warehouse_id = fields.Char(
        string="WAREHOUSEID"
    )
    accurate_customer_id = fields.Char(
        string="CUSTOMERID"
    )
    accurate_kode_warehouse = fields.Char(
        string="Kode Warehouse"
    )
    accurate_ar_account = fields.Char(
        string="PoS AR Account"
    )
    accurate_branch_code = fields.Char(
        string="PoS Branch Code"
    )
