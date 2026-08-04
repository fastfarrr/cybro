# -*- coding: utf-8 -*-
from odoo import models,fields,Command


class ProductProduct(models.Model):
    '''This class is inherited from product.product model '''
    _inherit='product.product'

    free_product=fields.Boolean(string="Free Product",default=False)


