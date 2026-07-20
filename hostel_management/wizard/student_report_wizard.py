 # -*- coding: utf-8 -*-
from odoo import models,fields
class StudentReportWizard(models.TransientModel):
     _name = 'student.report.wizard'
     _description = 'Student report have been created'


     student_id = fields.Many2one(comodel_name='student.details')
     room_id = fields.Many2one(comodel_name='hostel.room')

     def generate_pdf(self):
          self.ensure_one()
          return self.env.ref('hostel_management.action_student_report'
                              ).report_action(self)



