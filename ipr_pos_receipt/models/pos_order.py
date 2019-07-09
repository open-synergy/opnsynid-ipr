# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, _
from datetime import datetime
from openerp.exceptions import Warning as UserError


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.multi
    def reprint_receipt(self):
        res_params = {}
        str_date =\
            datetime.strptime(self.date_order, "%Y-%m-%d %H:%M:%S")
        format_date =\
            str_date.strftime("%d-%b-%Y")
        format_time =\
            str_date.strftime("%H:%M:%S")

        res_params = {
            "format_date": format_date,
            "format_time": format_time
        }

        action = self.env.ref(
            "proxy_backend_ecspos_aeroo."
            "proxy_backend_ecspos_aeroo_action")
        context = {
            "report_name": "aeroo_reportReprintReceipt",
            "object_id": [self.id],
            "params": res_params
        }
        result = action.read()[0]
        result.update({"context": context})
        return result
