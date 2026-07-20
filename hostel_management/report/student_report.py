# -*- coding:utf-8 -*-
from odoo import models
class StudentReport(models.AbstractModel):
    _name = 'student.report'
    _description = 'Report Created'

    def action_report_create(self):
        query="""select hr.room_number,hr.pending_amount,st.student_name,
        st.invoice_status from hostel_room as hr inner join 
        student_details as st on hr.id = st.room_id"""

        if self.room_id and self.student_id:
            query += "where st.room_id = '%s' and st.student_id = '%s'"


        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print("this is what comes in dict fetch all",report)
        data = {'room_id': self.read()[0],'report':report}
        return self.env.ref('hostel_management.action_student_report'
                            ).report_action(self, data=data)

