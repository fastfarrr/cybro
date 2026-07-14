#-*- coding: utf-8 -*-
from odoo import models,fields,Command,api

class NewItemRequest(models.Model):
    _name = 'new_item_request'
    _description = 'New Item Request'
    _rec_name = 'product_name'

    product_name=fields.Char(string="Product Name",required=True)
    product_cost=fields.Monetary(string="Product Cost")
    product_sale_price=fields.Monetary(string="Product Sale Price")
    currency_id=fields.Many2one('res.currency')
    partner_id=fields.Many2one('res.partner')
    requested_by=fields.Many2one('res.users',default=lambda self: self.env.user.id,readonly=True)
    state=fields.Selection([('draft','Draft'),
                            ('waiting','Waiting'),
                            ('approved','Approved')
                            ],default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        '''while creating record need to change the state'''
        for vals in vals_list:
            vals['state'] = 'waiting'
        return super().create(vals_list)

    def approve(self):
        '''while clicking approval need to change state and create a record in products'''
        self.state='approved'
        for order in self:
            self.env['product.product'].create({
                'sale_ok': True,
                'name': order.product_name,
                'standard_price': order.product_cost,
                'lst_price': order.product_sale_price,
            }
            )







