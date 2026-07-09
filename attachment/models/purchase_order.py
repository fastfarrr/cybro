from odoo import models, fields, api
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    """class for purchase order"""
    _inherit = "purchase.order"

    is_file_valid = fields.Boolean(string="Attachment",
                                   compute="_compute_is_file_valid",
                                   tracking=True)


    # @api.depends('message_attachment_count')
    # def _compute_show_warning_message(self):
    #     """To show warning message based on settings"""
    #     show_warning=(self.env['ir.config_parameter'].
    #                   sudo().
    #                   get_param('Attachment.is_file_attached') == True)
    #
    #     print(show_warning)
    #
    #     for order in self:
    #         # order.show_warning_message=show_warning and not order.is_file_valid
    #         if show_warning:
    #             order.is_file_valid = False
    #         elif:
    #             or
    #         else:
    #             order.show_warning_message=True





    @api.depends('message_attachment_count')
    def _compute_is_file_valid(self):
        """check the file valid or not depended on attachment_count"""
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
            print("gfh", order.is_file_valid)




    def button_confirm(self):
        "checking is there any attachment attached to chatter"
        required_attachment = (self.env['ir.config_parameter']
                               .sudo().get_param('Attachment.is_file_attached'))

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





