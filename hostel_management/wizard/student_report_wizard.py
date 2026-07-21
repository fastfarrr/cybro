# -*- coding: utf-8 -*-
from odoo import models, fields


class StudentReportWizard(models.TransientModel):
    """class that is to store values for student report wizard
    created as  transient model """
    _name = 'student.report.wizard'
    _description = 'Student report have been created'

    room_id = fields.Many2many(comodel_name='hostel.room')
    student_id = fields.Many2many(comodel_name='student.details',
                                 domain="[('room_id', '=', room_id)]")

    def generate_pdf(self):
        """While clicking generate PDF button it should trigger the
        inbuilt report action to create PDF"""
        self.ensure_one()
        return self.env.ref('hostel_management.action_student_report'
                            ).report_action(self)

    def action_report_create(self):
        """linked with action report it helps to sort the datas inside
        the table and this will pass the values into PDF"""
        query = """ select hr.id,hr.room_number,hr.pending_amount,st.student_name,
         st.invoice_status from hostel_room as hr inner join 
         student_details as st on hr.id = st.room_id """
        # query = """ select hr.room_number,am.amount_residual,st.student_name,
        #  st.invoice_status from hostel_room as hr inner join
        #  student_details as st on hr.id = st.room_id inner join
		#  account_move as am on hr.invoice_id = am.student_id """
        print(query)

        if self.room_id and self.student_id:
            query += """where st.room_id = '%s' and st.student_id = '%s'"""

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data = {'report': report}
        return self.env.ref('hostel_management.action_student_report'
                            ).report_action(None,data=data)
