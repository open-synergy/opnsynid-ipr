# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import time
from openerp.report import report_sxw
import pytz
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            "time": time,
            "get_date_start": self._get_date_start,
            "get_date_end": self._get_date_end,
            "get_data": self._get_data,
        })

    def _convert_datetime_utc(self, dt):
        if dt:
            obj_user = self.pool.get('res.users')
            user = obj_user.browse(self.cr, self.uid, [self.uid])[0]
            convert_dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            if user.tz:
                tz = pytz.timezone(user.tz)
            else:
                tz = pytz.utc
            convert_utc = pytz.utc.localize(convert_dt).astimezone(tz)
            format_utc = convert_utc.strftime("%d-%B-%Y %H:%M:%S")

            return format_utc
        else:
            return "-"

    def _get_date_start(self):
        data = self.localcontext['data']['form']
        date_start = data['date_start']

        return self._convert_datetime_utc(
            date_start)

    def _get_date_end(self):
        data = self.localcontext['data']['form']
        date_start = data['date_end']

        return self._convert_datetime_utc(
            date_start)

    def set_context(self, objects, data, ids, report_type=None):
        self.form = data["form"]
        self.date_start = self.form["date_start"]
        self.date_end = self.form["date_end"]
        self.warehouse_ids = self.form["warehouse_ids"]
        self.warehouse_dest_ids = self.form["warehouse_dest_ids"]
        self.product_ids = self.form["product_ids"]
        return super(Parser, self).set_context(objects, data, ids, report_type)

    def _get_data(self):
        data = []
        obj_data = self.pool.get(
            "stock.move_transfer_list")
        no = 1

        criteria = [
            ("source_loc_wh_id", "in", self.warehouse_ids),
            ("source_dest_loc_wh_id", "in", self.warehouse_dest_ids),
        ]

        if self.date_start and self.date_end:
            criteria += [
                ("date", ">=", self.date_start),
                ("date", "<=", self.date_end),
            ]
        elif not self.date_start and self.date_end:
            criteria += [
                ("date", "<=", self.date_end),
            ]
        elif self.date_start and not self.date_end:
            criteria += [
                ("date", ">=", self.date_start),
            ]

        if self.product_ids:
            criteria += [
                ("product_id", "in", self.product_ids)
            ]

        data_ids = obj_data.search(self.cr, self.uid, criteria)

        if data_ids:
            for data_id in obj_data.browse(
                self.cr,
                self.uid,
                data_ids
            ):
                picking_id = data_id.picking_id
                internal_ref = picking_id and picking_id.name or "-"

                product_id = data_id.product_id
                product_name = product_id and product_id.name or "-"

                uom_id = data_id.product_uom_id
                uom_name = uom_id and uom_id.name or "-"

                source_loc_wh_id = data_id.source_loc_wh_id
                source_loc_wh_name = (
                    source_loc_wh_id and
                    source_loc_wh_id.name or
                    "-"
                )

                source_dest_loc_wh_id = data_id.source_dest_loc_wh_id
                source_dest_loc_wh_name = (
                    source_dest_loc_wh_id and
                    source_dest_loc_wh_id.name or
                    "-"
                )

                conv_date = self._convert_datetime_utc(
                    data_id.date)

                res = {
                    "no": no,
                    "internal_ref": internal_ref,
                    "product_code": data_id.product_code,
                    "product_name": product_name,
                    "qty": data_id.product_qty,
                    "uom": uom_name,
                    "src_loc": source_loc_wh_name,
                    "dest_loc": source_dest_loc_wh_name,
                    "date": conv_date,
                }
                data.append(res)
                no += 1

        return data
