# -*- coding: utf-8 -*-
from odoo import models, fields


class Move(models.Model):
    _inherit = "account.move"
    student_id = fields.Many2one('student.details',
                                 string="Student")

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

    def _send_monthly_invoice(self):
        students=self.env['student.details'].search([
            ('room_id','!=','False'),
            ('email', '!=','False')
        ])

        product = self.env.ref(
            'hostel_management.rental_product1',
            raise_if_not_found=False
        )

        if not product:
            return

        for student in students:
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': student.partner_id.id,
                'student_id': student.id,
                'invoice_line_ids': [(0, 0, {
                    'product_id': product.id,
                    'quantity': 1,
                    'price_unit': student.room_id.rent,
                })],
            })

            invoice.action_post()