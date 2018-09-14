# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields, _
from openerp.exceptions import Warning as UserError
import pytz
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class PrintRekapBill(models.TransientModel):
    _name = "pos.order_print_rekap_bill"

    date = fields.Date(
        string="Date",
        required=True,
        default=datetime.now().strftime("%Y-%m-%d"),
    )
    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        required=True
    )

    @api.multi
    def _convert_datetime_utc(self, dt):
        self.ensure_one()
        convert_dt = datetime.strptime(
            dt, DEFAULT_SERVER_DATETIME_FORMAT)

        if self.env.user.tz:
            tz = pytz.timezone(self.env.user.tz)
        else:
            return False

        convert_tz = tz.localize(convert_dt)
        convert_utc = convert_tz.astimezone(pytz.utc)
        format_utc = datetime.strftime(
            convert_utc,
            DEFAULT_SERVER_DATETIME_FORMAT
        )

        return format_utc

    @api.multi
    def print_rekap_bill(self):
        obj_pos_order = self.env["pos.order"]
        date_start_utc =\
            self._convert_datetime_utc(self.date + ' 00:00:00')
        date_stop_utc =\
            self._convert_datetime_utc(self.date + ' 23:59:59')

        criteria = [
            ("picking_type_id.warehouse_id", "=", self.warehouse_id.id),
            ("date_order", ">=", date_start_utc),
            ("date_order", "<=", date_stop_utc),
            ("state", "in", ["paid", "done"])
        ]

        pos_order =\
            obj_pos_order.search(criteria, order="pos_reference asc")

        if pos_order:
            str_date =\
                datetime.strptime(self.date, "%Y-%m-%d")
            format_date =\
                str_date.strftime("%d-%b-%Y")
            res_params = {
                "warehouse": self.warehouse_id.name,
                "date": format_date
            }
            action = self.env.ref(
                "proxy_backend_ecspos_aeroo."
                "proxy_backend_ecspos_aeroo_action")
            context = {
                "report_name": "aeroo_reportRekapBill",
                "object_id": pos_order.ids,
                "print_type": "continuous",
                "params": res_params
            }
            result = action.read()[0]
            result.update({"context": context})
            return result
        else:
            raise UserError(_("No Data"))
