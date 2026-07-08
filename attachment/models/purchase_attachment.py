# # -*- coding: utf-8 -*-
from odoo import models,fields
class PurchaseConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_file_attached=fields.Boolean(string="Purchase Attachment",default=False)

    def set_values(self):
        super(PurchaseConfigSettings,self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'Attachment.is_file_attached',self.is_file_attached
        )

    def get_values(self):
        res=super(PurchaseConfigSettings,self).get_values()
        value=self.env['ir.config_parameter'].sudo().get_param(
            'Attachment.is_file_attached'
        )
        res.update(is_file_attached=value)
        return res
