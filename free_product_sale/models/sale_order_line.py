# -*- coding: utf-8 -*-
from odoo import models,fields

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _description = "Sale Order Line"

    product_id = fields.Many2one('product.product')
    sale_order_id = fields.Many2one('sale.order')
    free_product=fields.Boolean(related="product_id.free_product")
    excluded_product_ids=fields.Many2many(related="sale_order_id.excluded_product_ids")


    def exclude_free_products(self):

        if self.free_product:
            stored_free_product=self.product_id
            print('stored product',stored_free_product)

            self.order_id = self.sale_order_id.id

            a=self.write({
                'excluded_product_ids':[(fields.Command.link(stored_free_product.id))]
            })
            print(a)
            self.unlink()

        else:
            print('got some issue while unlinking')










