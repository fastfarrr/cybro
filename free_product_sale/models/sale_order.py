# -*- coding : UTF-8 -*-
from odoo import models, fields, Command
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    '''This class is inherited  from sale order'''
    _inherit = 'sale.order'
    free_product_id = fields.Many2one('product.product')
    free_product = fields.Boolean(related='free_product_id.free_product')

    def check_free_product(self):
        '''This function works when the button is clicked'''
        product = self.env['product.product'].search(
            [('free_product', '=', True)])
        print(product)

        for product in product:

            if product not in self.order_line.product_id:
                self.write({'order_line': [Command.create({
                    'product_id': product.id,
                    'name': product.name,
                    'product_uom_qty': 1,
                    'price_unit': 0,
                    'tax_ids': [],
                })]})




            print('these are the products which are free', product)


        if not product:
            raise ValidationError("No product is configured")

        # if product:
        #     for rec in product:
        #         self.write({
        #             'order_line': [Command.create({
        #                 'product_id': rec.id,
        #                 'name': rec.name,
        #                 'product_uom_qty': 1,
        #                 'price_unit': 0,
        #                 'tax_ids': [],
        #             })]})

        # if not product:
        #     raise ValidationError("No product is configured")
        #
        # existing = self.order_line.filtered(lambda s: s.product_id in product)
        # print('these are the product inside invoice line', existing)
