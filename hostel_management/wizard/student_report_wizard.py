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
    room_number = fields.Char(related='room_id.room_number')
    student_name = fields.Char(related='student_id.student_name')



    def generate_pdf(self):
        """While clicking generate PDF button it should trigger function which contains psql query"""
        self.ensure_one()
        return self.action_report_create()

    def action_report_create(self):
        """linked with action report it helps to sort the datas inside
        the table and this will pass the values into PDF"""
        query = """ select hr.id as room_id,st.id as student_id,
        hr.room_number,SUM(am.amount_residual)as pending_amount,
        st.student_name,case when(SUM(am.amount_residual)>0) then 'pending' else  'done' end as invoice_status
        from hostel_room as hr inner join student_details as st on hr.id = st.room_id left join account_move as am on am.student_id = st.id group by hr.id,st.id"""


        if self.room_id and self.student_id:
            query += """ having hr.id in %s and st.id in %s """



        self.env.cr.execute(query,(tuple(self.room_id.ids),tuple(self.student_id.ids)))
        report = self.env.cr.dictfetchall()
        data = {'student_name':self.student_name,'room_number':self.room_number,'report': report}
        # data={'report':report}
        print(data)
        return self.env.ref('hostel_management.action_student_report'
                            ).report_action(None,data=data)


