from odoo import models, fields, api
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    """class to inherit for purchase order"""
    _inherit = "purchase.order"

    is_file_valid = fields.Boolean(string="Attachment",
                                   compute="_compute_is_file_valid",)
    is_file_attached = fields.Boolean(string="Attachment",
                                      compute="_compute_is_file_attached")
    def _compute_is_file_attached(self):
        """To make the alert invisible if setting value is true"""
        setting_val = (self.env['ir.config_parameter']
                       .sudo()
                       .get_param('purchase_order_attachment.is_file_attached') == 'True')
        for order in self:
            order.is_file_attached = setting_val


    @api.depends('message_attachment_count')
    def _compute_is_file_valid(self):
        """computing is attached file valid or not"""
        for order in self:
            attachment=self.env['ir.attachment'].search(
                [('res_model', '=', 'purchase.order'),
                 ('res_id', '=', order.id),
                 ('mimetype', 'in', ('application/pdf',
                                     'image/png',
                                     'image/jpeg',
                                     'image/jpg'))
                ]
            )
            order.is_file_valid = attachment

    def button_confirm(self):
        """Checking is there any purchase_order_attachment attached to chatter"""
        required_attachment = (self.env['ir.config_parameter']
                               .sudo().get_param('purchase_order_attachment.is_file_attached'))


        if required_attachment == 'True':
            for order in self:
                attachment = self.env["ir.attachment"].search(
                    [('res_model', '=', 'purchase.order'),
                     ('res_id', '=', order.id),
                     ('mimetype', 'in', ('application/pdf', 'image/png',
                                         'image/jpeg', 'image/jpg')),
                     ]
                )

                if not attachment:
                    raise UserError("Please attach at least one image or pdf")

        return super().button_confirm()





