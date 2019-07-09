# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.subtotal = 0.0
        self.change = 0.0
        self.paid = 0.0
        self.res_taxes = {}
        self.res_payment_lines = {}
        self.localcontext.update({
            "time": time,
            "compute_price":self._compute_price,
            "get_subtotal":self._get_subtotal,
            "get_taxes":self._get_taxes,
            "compute_payment_lines": self._compute_payment_lines,
            "get_payment_lines":self._get_payment_lines,
            "get_change":self._get_change,
            "get_paid":self._get_paid
        })

    def calculate_tax(self, pos_order, unit_price, qty):
        val = invoice_line_id.invoice_line_tax_id.compute_all(
            unit_price,
            qty,
            invoice_line_id.product_id,
            invoice_line_id.partner_id
        )
        return val

    def _compute_price(self, unit_price, qty, discount):
        price = unit_price * qty * (1 - discount/100)
        self.subtotal += price
        return price

    def _get_subtotal(self):
        return self.subtotal
    
    def _get_taxes(self, order_lines):
        obj_account_tax = self.pool.get('account.tax')
        for line in order_lines:
            if line.product_id.pos_tax_ids:
                taxes_id = line.product_id.pos_tax_ids
            else:
                taxes_id = line.product_id.taxes_id
            if taxes_id:
                taxes_ids = [tax for tax in taxes_id if tax.company_id.id == line.order_id.company_id.id]
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = obj_account_tax.compute_all(
                    self.cr,
                    self.uid,
                    taxes_ids,
                    price, line.qty,
                    product=line.product_id,
                    partner=line.order_id.partner_id or False
                )
                cur = line.order_id.pricelist_id.currency_id
                for tax in taxes['taxes']:
                    id = tax['id']
                    if id not in self.res_taxes:
                        t = obj_account_tax.browse(self.cr, self.uid, id, context={})
                        tax_rule = ''
                        if t.type == 'percent':
                            tax_rule = str(100 * t.amount) + '%'
                        else:
                            tax_rule = str(t.amount)
                        self.res_taxes[id] = {
                            'name': tax['name'],
                            'base': 0,
                            'tax': tax_rule,
                            'total': 0,
                        }
                    self.res_taxes[id]['base'] += cur.round(tax['price_unit'] * line.qty)
                    self.res_taxes[id]['total'] += tax['amount']
        return self.res_taxes.values()

    def _compute_payment_lines(self, statement_ids):
        for payment_lines in statement_ids:
            id = payment_lines.journal_id.id
            if id not in self.res_payment_lines:
                if payment_lines.journal_id.pos_journal_display_name:
                    name = payment_lines.journal_id.pos_journal_display_name
                else:
                    name = payment_lines.journal_id.name
                self.res_payment_lines[id] = {
                    'name': name,
                    'total': 0
                }
            if payment_lines.amount > 0:
                self.res_payment_lines[id]['total'] += payment_lines.amount
                self.paid += payment_lines.amount
            else:
                self.change += abs(payment_lines.amount)

    def _get_payment_lines(self):
        return self.res_payment_lines.values()

    def _get_change(self):
        return self.change

    def _get_paid(self):
        return self.paid
