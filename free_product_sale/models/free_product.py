# -*- coding: utf-8 -*-
from odoo import models,fields,Command


class FreeProductSale(models.Model):
    _inherit='product.product'

    free_product=fields.Boolean(string="Free Product",default=False)

    def check_free_product(self):
        product=self.search([])
        new=product.filtered(lambda p:p.free_product)
        if new:
            order_line={'invoice_line_ids':[Command.create({
                'product_template_id':new.id,
                'quantity':1,
                'price_unit':0
            })]}





