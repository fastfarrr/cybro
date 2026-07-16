# -*- coding: utf-8 -*-
from odoo import fields,models
class ProductTemplateAttributeLine(models.Model):
    _name = 'product.template.attribute.variant'
    _description = 'Product variant created'

    variant_id = fields.Many2one(comodel_name='new_item_request')
    attribute_id = fields.Many2one(comodel_name='product.attribute')
    value_ids = fields.Many2many(comodel_name='product.attribute.value',
        relation='product_attribute_value_product_template_attribute_variant_rel',
        string="Values",
        domain="[('attribute_id', '=', attribute_id)]",
        ondelete='restrict')


