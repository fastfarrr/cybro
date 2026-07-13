#-*- coding: utf-8 -*-
from odoo import models, fields,api

class PurchaseOrder(models.Model):
    """This class inherited the model purchase.order """
    _inherit = "purchase.order"

    is_vendor_product = fields.Boolean(string="Vendor Products")
    product_ids=fields.Many2many(comodel_name='product.product',compute='_compute_product_ids')

    @api.depends('is_vendor_product','partner_id')
    def _compute_product_ids(self):
        for order in self:
            if order.is_vendor_product and order.partner_id:
                products=self.env['product.product'].search([
                    ('product_tmpl_id.seller_ids.partner_id'
                         , '='
                         , self.partner_id.id)
                ])
            else:
                products = self.env['product.product'].search([
                                    ('purchase_ok', '=', True)
                                ])
            order.product_ids = products



    # @api.onchange('partner_id','is_vendor_product')
    # def _onchange_vendor_products(self):
    #     products = self.env['product.product'].search([
    #         ('product_tmpl_id.seller_ids.partner_id', '=', self.partner_id.id)
    #     ])
    #     print(products)
    #     if self.is_vendor_product:
    #         self.order_line = [Command.clear()]
    #         for product in products:
    #             self.order_line = [
    #                 Command.create({
    #                     'product_id': product.id,
    #                     'product_qty':1,
    #                     'price_subtotal':product.standard_price
    #                 })
    #             ]
    #     else:
    #         self.order_line = [Command.clear()]
    #         self.order_line = [Command.create({
    #             'product_id': []
    #         })]




