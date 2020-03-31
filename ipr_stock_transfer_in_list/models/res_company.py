# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    allowed_transfer_in_product_ids = fields.Many2many(
        string="Allowed Transfer In Products",
        comodel_name="product.product",
        relation="rel_company_2_transfer_in_product",
        column1="company_id",
        column2="product_id",
    )
    allowed_transfer_in_product_categ_ids = fields.Many2many(
        string="Allowed Transfer In Product Categories",
        comodel_name="product.category",
        relation="rel_company_2_transfer_in_product_categ",
        column1="company_id",
        column2="category_id",
    )
