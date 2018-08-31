# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.total = 0.00
        self.localcontext.update({
            "time": time,
            "get_data": self._get_data,
            "get_branch_code": self.get_branch_code,
            "get_ar_account": self.get_ar_account,
            "get_accurate_info": self.get_accurate_info,
            "get_invoice_no": self.get_invoice_no,
            "get_date": self.get_date,
            "get_description": self.get_description,
            "get_total": self.get_total,
        })

    def set_context(self, objects, data, ids, report_type=None):
        self.form = data["form"]
        self.description = self.form["description"]
        self.accurate_invoice_no = self.form["accurate_invoice_no"]
        self.warehouse_id = self.form["warehouse_id"][0]
        self.date = self.form["date"]
        return super(Parser, self).set_context(objects, data, ids, report_type)

    def get_invoice_no(self):
        return self.accurate_invoice_no

    def get_date(self):
        return self.date

    def get_description(self):
        return self.description

    def get_total(self):
        return self.total

    def get_branch_code(self):
        obj_user = self.pool.get("res.users")
        user = obj_user.browse(self.cr, self.uid, [self.uid])[0]

        return user.company_id.accurate_branch_code

    def get_ar_account(self):
        obj_user = self.pool.get("res.users")
        user = obj_user.browse(self.cr, self.uid, [self.uid])[0]

        return user.company_id.accurate_pos_ar_account

    def get_accurate_info(self):
        res={}
        obj_wh = self.pool.get("stock.warehouse")
        criteria = [
            ("id", "=", self.warehouse_id)
        ]
        warehouse_id = obj_wh.search(self.cr, self.uid, criteria)
        if warehouse_id:
            wh =\
                obj_wh.browse(self.cr, self.uid, warehouse_id)
            if wh.accurate_dept_id:
                res["accurate_dept_id"] = wh.accurate_dept_id
            else:
                res["accurate_dept_id"] = ""
            if wh.accurate_warehouse_id:
                res["accurate_warehouse_id"] = wh.accurate_warehouse_id
            else:
                res["accurate_warehouse_id"] = ""
            if wh.accurate_customer_id:
                res["accurate_customer_id"] = wh.accurate_customer_id
            else:
                res["accurate_customer_id"] = ""
        return res

    def _get_data(self):
        data = []
        obj_data = self.pool.get(
            "pos.order_summary")
        ascii_date_order =\
            self.date.encode("ascii")

        criteria = [
            ("warehouse_id", "=", self.warehouse_id),
            ("date_order", "=", ascii_date_order)
        ]

        data_ids = obj_data.search(self.cr, self.uid, criteria)

        if data_ids:
            for data_id in obj_data.browse(self.cr, self.uid, data_ids):
                product = data_id.product_id
                res = {
                    "key_id": data_id.id,
                    "item_no": product.code or "",
                    "total_qty": data_id.total_qty,
                    "itemovdesc": product.name or "",
                    "unit_price": data_id.price_unit or "",
                    "total_price": data_id.total_price,
                    "category": product.categ_id.name or "",
                    "total_discount": data_id.total_discount
                }
                self.total = self.total + data_id.total_price
                data.append(res)

        return data
