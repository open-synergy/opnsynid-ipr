# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
import pytz
from openerp.report import report_sxw
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.list_config = []
        self.list_category = []
        self.localcontext.update({
            "time": time,
            "get_company": self._get_company,
            "get_date": self._get_date,
            "get_pos_config": self._get_pos_config,
            "get_category": self._get_category,
            "get_lines": self._get_lines
        })

    def set_context(self, objects, data, ids, report_type=None):
        self.form = data["form"]
        self.company_id = self.form["company_id"][0]
        self.date = self.form["date"]
        self.config_ids = self.form["config_ids"]
        return super(Parser, self).set_context(objects, data, ids, report_type)

    def _convert_datetime_utc(self, dt):
        obj_user = self.pool.get("res.users")
        user = obj_user.browse(self.cr, self.uid, [self.uid])[0]
        convert_dt = datetime.strptime(dt, DEFAULT_SERVER_DATETIME_FORMAT)

        if user.tz:
            tz = pytz.timezone(user.tz)
            convert_tz = tz.localize(convert_dt)
            convert_utc = convert_tz.astimezone(pytz.utc)
            format_utc = datetime.strftime(
                convert_utc,
                DEFAULT_SERVER_DATETIME_FORMAT
            )
        else:
            format_utc = dt
        return format_utc

    def _get_company(self):
        obj_res_company = self.pool.get("res.company")

        company = obj_res_company.browse(
            self.cr, self.uid, self.company_id
        )

        return company

    def _get_date(self):
        return self.date

    def _get_pos_config(self):
        obj_pos_config = self.pool.get("pos.config")

        if self.config_ids:
            for config in obj_pos_config.browse(
                    self.cr, self.uid, self.config_ids):
                res = {
                    "id": config.id,
                    "name": config.name,
                }
                self.list_config.append(res)

        return self.list_config

    def _get_category(self):
        obj_pos_category = self.pool.get("pos.category")

        categ_ids = obj_pos_category.search(
            self.cr, self.uid, [])

        categ = obj_pos_category.browse(
            self.cr, self.uid, categ_ids)

        return categ

    def _get_lines(self, config_id, categ):
        total = 0.00
        detail = []
        lines = []
        list_product = []
        obj_order_line_summary =\
            self.pool.get(
                "pos.order_line_summary"
            )

        date_1 = self._convert_datetime_utc(
            dt=self.date + " " + "00:00:00"
        )
        date_2 = self._convert_datetime_utc(
            dt=self.date + " " + "23:59:59"
        )

        criteria = [
            ("config_id", "=", config_id),
            ("date_order", ">=", date_1),
            ("date_order", "<=", date_2),
            ("pos_categ_id", "=", categ.id)
        ]

        sumarry_line_ids = obj_order_line_summary.search(
            self.cr, self.uid, criteria
        )

        if sumarry_line_ids:
            summary_line = obj_order_line_summary.browse(
                self.cr, self.uid, sumarry_line_ids)

            for line in summary_line:
                product_id = line.product_id.id,
                product_name = line.product_id.name
                qty = line.qty
                subtotal = line.price_subtotal
                if not detail:
                    res = {
                        "product_id": product_id,
                        "product": product_name,
                        "qty": qty,
                        "subtotal": subtotal,
                    }
                    list_product.append(product_id)
                    detail.append(res)
                else:
                    if product_id in list_product:
                        for product in detail:
                            if product["product_id"] == product_id:
                                product["qty"] += qty
                                product["subtotal"] += subtotal
                    else:
                        res = {
                            "product_id": product_id,
                            "product": product_name,
                            "qty": qty,
                            "subtotal": subtotal,
                        }
                        list_product.append(product_id)
                        detail.append(res)
                total += subtotal

            value = {
                "category": categ.name,
                "total": total,
                "detail": detail
            }
            lines.append(value)
        return lines
