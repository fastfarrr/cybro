from odoo import models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit= ["purchase.order"]

    def button_confirm(self):
        for order in self:
            attachment=self.env["ir.attachment"].search(
                [('res_model', '=', 'purchase.order'),
                 ('res_id', '=', order.id),
                 ('mimetype','in',('application/pdf','image/png',
                                   'image/jpeg','image/jpg')),
                ]
            )
            if not attachment:
                raise UserError("Please attach at least a file")

        return super().button_confirm()



