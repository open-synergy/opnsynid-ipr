# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class RestaurantPrinter(models.Model):
    _inherit = "restaurant.printer"

    print_rekap_bill = fields.Boolean(
        string="Print Rekap Bill"
    )
