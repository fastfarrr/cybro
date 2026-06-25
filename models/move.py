# -*- coding: utf-8 -*-
from odoo import models, fields


class Move(models.Model):
    _inherit = "account.move"
    student_id = fields.Many2one('student.details', string="Student")

    def action_post(self):
        res = super().action_post()

        template = self.env.ref('hostel_management.invoice_email_template')

        for invoice in self:
            if invoice.student_id and invoice.student_id.email:
                email_values = {
                    'email_to': invoice.student_id.email,
                    'email_from': self.env.user.email,
                }
                template.send_mail(
                    invoice.id,
                    force_send=True,
                    email_values=email_values
                )

        return res




