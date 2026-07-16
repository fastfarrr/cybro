# -*- coding: utf-8 -*-
from odoo import models, fields,Command


class NewItemRequest(models.Model):
    '''A model to create a new item request in sales module
     which is regular model'''
    _name = 'new_item_request'
    _description = 'New Item Request'
    _rec_name = 'product_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    product_name = fields.Char(string="Product Name", required=True)
    product_cost = fields.Monetary(string="Product Cost")
    product_sale_price = fields.Monetary(string="Product Sale Price", required=True)
    company_id = fields.Many2one('res.company',
                                 string="Company",
                                 default=lambda self
                                 : self.env.user.company_id.id)
    currency_id = fields.Many2one(comodel_name='res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self:
                                  self.env.user.company_id.currency_id.id
                                  )
    requested_by = fields.Many2one(comodel_name='res.users',
                                   default=lambda self: self.env.user.id,
                                   readonly=True)
    state = fields.Selection(selection=[('draft', 'Draft'),
                              ('waiting', 'Waiting'),
                              ('approved', 'Approved'),('rejected', 'Rejected')
                              ], default='draft',tracking=True)

    value_ids = fields.One2many(comodel_name='product.template.attribute.variant',inverse_name='variant_id')

    def approve(self):
        '''while clicking approval need to change state and
        create a record in products'''
        self.write({'state': 'approved'})
        for order in self:
            product=self.env['product.template'].create({
                'sale_ok': True,
                'name': order.product_name,
                'standard_price': order.product_cost,
                'list_price': order.product_sale_price,
            }
            )
            for line in order.value_ids:
                self.env['product.template.attribute.line'].create({
                'product_tmpl_id':product.id,
                'attribute_id': line.attribute_id.id,
                'value_ids': [Command.set(line.value_ids.ids)],
                })

    def to_approve(self):
        '''While clicking to approve button it should change
         the state to waiting'''
        self.write({'state':'waiting'})

    def to_reject(self):
        '''While clicking to reject button it should change
        the state to rejected'''
        self.write({'state':'rejected'})
