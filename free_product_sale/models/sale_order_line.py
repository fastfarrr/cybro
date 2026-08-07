# -*- coding: utf-8 -*-
from odoo import models,fields

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _description = "Sale Order Line"

    product_id = fields.Many2one('product.product')
    free_product=fields.Boolean(related="product_id.free_product")


    def exclude_free_products(self):

        if self.free_product:
            stored_free_product=self.product_id

            self.order_id.write({'excluded_product_ids':[(fields.Command.link(stored_free_product.id))]})
            self.unlink()










