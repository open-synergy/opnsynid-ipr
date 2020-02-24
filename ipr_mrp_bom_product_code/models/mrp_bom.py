# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    product_code = fields.Char(
        string="Product Code",
        related="product_id.default_code",
        store=False,
        readonly=True,

    )
