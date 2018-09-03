# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID
from openerp.api import Environment


def migrate(cr, version):
    if not version:
        return

    cr.execute("""
        DELETE FROM ir_model_data
        WHERE   name = 'field_accurate_pos_ar_account' AND
                module = 'res.company' AND
                model = 'ir.model.fields'
        """)

    cr.execute("""
        DELETE FROM ir_model_fields AS a
        USING    ir_model AS b
        WHERE   a.name = 'accurate_pos_ar_account' AND
                b.model = 'res.company' AND
                a.model_id = b.id
        """)

    cr.execute("""
        ALTER TABLE res_company
        DROP COLUMN IF EXISTS accurate_pos_ar_account
    """)
