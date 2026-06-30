from odoo import models

class ResUsers(models.Model):
    _inherit = 'res.users'
    # def _create_user(self):
    #     students = self.env['student.details'].search([
    #         ('user_id', '=', False)
    #     ])
    #
    #     for student in students:
    #         user = self.create({
    #             'name': student.student_name,
    #             'login': student.email,
    #             'email': student.email,
    #             'password': 'demo431',
    #             'partner_id': student.partner_id.id,
    #         })
    #         student.user_id = user.id