# -*- coding: utf-8 -*-
from odoo import fields,models
class Company(models.Model):
    """inherited company model for company dependent"""
    _inherit = 'res.company'
    limit = fields.Boolean(string="limit")
    discount_limit = fields.Float(string="Discount Limit",default=0)

