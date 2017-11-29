# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
import pytz
from openerp.report import report_sxw
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.list_config = []
        self.localcontext.update({
            "time": time,
            "get_company": self._get_company,
            "get_date": self._get_date,
            "get_pos_config": self._get_pos_config,
            "get_pos_order": self._get_pos_order,
        })

    def set_context(self, objects, data, ids, report_type=None):
        self.form = data["form"]
        self.company_id = self.form["company_id"][0]
        self.date = self.form["date"]
        self.config_ids = self.form["config_ids"]
        return super(Parser, self).set_context(objects, data, ids, report_type)

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

    def time_range(self):
        time_list = []
        for x in range(0, 24):
            if x == 23:
                res_time = {
                    'start_time': timedelta(hours=1*x),
                    'end_time': timedelta(hours=23, minutes=59, seconds=59)
                }
            else:
                res_time = {
                    'start_time': timedelta(hours=1*x),
                    'end_time': timedelta(hours=1*x, minutes=59, seconds=59)
                }
            time_list.append(res_time)
        return time_list

    def _convert_datetime_utc(self, dt):
        obj_user = self.pool.get('res.users')
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

    def _get_pos_order(self, config_id):
        value = {}
        list_order = []
        obj_pos_order = self.pool.get("pos.order")

        if config_id:
            for time_range in self.time_range():
                customer_dine_in = 0
                customer_take_away = 0
                amount_dine_in = 0.0
                amount_take_away = 0.0
                average_take_away = 0.0
                average_dine_in = 0.0
                start_time = str(time_range['start_time'])
                end_time = str(time_range['end_time'])

                date_1 = self._convert_datetime_utc(
                    dt=self.date + ' ' + start_time
                )
                date_2 = self._convert_datetime_utc(
                    dt=self.date + ' ' + end_time
                )

                criteria = [
                    ('session_id.config_id', '=', config_id),
                    ('date_order', '>=', date_1),
                    ('date_order', '<=', date_2),
                    ('state', 'not in', ['draft', 'cancel'])
                ]

                order_ids = obj_pos_order.search(
                    self.cr, self.uid, criteria
                )

                if order_ids:
                    for order in obj_pos_order.browse(
                            self.cr, self.uid, order_ids):
                        if order.table_id:
                            if order.guest > 0:
                                customer_dine_in += order.guest
                            else:    
                                customer_dine_in += 1
                            amount_dine_in += order.amount_total
                        else:
                            customer_take_away += 1
                            amount_take_away += order.amount_total

                    if customer_dine_in > 0:
                        average_dine_in = (amount_dine_in / customer_dine_in)
                    if customer_take_away > 0:
                        average_take_away =\
                            (amount_take_away / customer_take_away)
                    value = {
                        "hours": start_time + ' - ' + end_time,
                        "dine_in": {
                            "customer": customer_dine_in,
                            "amount": amount_dine_in,
                            "average": round(average_dine_in, 3)
                        },
                        "take_away": {
                            "customer": customer_take_away,
                            "amount": amount_take_away,
                            "average": round(average_take_away, 3)
                        },
                        "total_customer": (
                            customer_dine_in + customer_take_away),
                        "total_net": amount_dine_in + amount_take_away
                    }
                    list_order.append(value)

        return list_order
