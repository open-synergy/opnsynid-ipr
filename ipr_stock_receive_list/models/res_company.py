# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    allowed_receive_product_ids = fields.Many2many(
        string="Allowed Receive Products",
        comodel_name="product.product",
        relation="rel_company_2_receive_product",
        column1="company_id",
        column2="product_id",
    )
    allowed_receive_product_categ_ids = fields.Many2many(
        string="Allowed Receive Product Categories",
        comodel_name="product.category",
        relation="rel_company_2_receive_product_categ",
        column1="company_id",
        column2="category_id",
    )
