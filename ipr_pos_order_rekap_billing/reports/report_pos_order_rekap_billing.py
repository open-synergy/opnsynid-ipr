# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from openerp.report import report_sxw
from datetime import datetime
import pytz


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.total = 0.00
        self.total_v2 = 0.00
        self.sub_total = 0.00
        self.discount = 0.00
        self.refund = 0.00
        self.localcontext.update({
            "time": time,
            "compute_discount":self._compute_discount,
            "get_discount":self._get_discount,
            "compute_sub_total":self._compute_sub_total,
            "get_sub_total":self._get_sub_total,
            "compute_total":self._compute_total,
            "get_total":self._get_total,
            "compute_refund":self._compute_refund,
            "get_refund":self._get_refund,
            "get_net_sales":self._get_net_sales,
            "convert_datetime_utc":self._convert_datetime_utc,
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
            format_utc = convert_utc.strftime("%H:%M:%S")

            return format_utc
        else:
            return "-"

    def _compute_discount(self, discount):
        self.discount +=  discount

    def _get_discount(self):
        return self.discount

    def _compute_sub_total(self, price_subtotal):
        self.sub_total +=  price_subtotal

    def _get_sub_total(self):
        result = self.sub_total
        self.sub_total = 0.00
        return result

    def _compute_total(self, total):
        self.total +=  total

    def _get_total(self):
        self.total_v2 = self.total - self.refund
        return self.total_v2

    def _compute_refund(self, refund):
        self.refund +=  refund

    def _get_refund(self):
        return self.refund

    def _get_net_sales(self):
        return self.total_v2 - (self.discount + self.refund)