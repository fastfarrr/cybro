# -*- coding: utf-8 -*-
from odoo import models,fields


class LeaveRequestWizard(models.TransientModel):
    """Class that is to store values for leave request wizard created
    as  transient model"""
    _name = 'leave.request.report.wizard'

    room_id = fields.Many2one(comodel_name='hostel.room')
    student_id = fields.Many2many(comodel_name='student.details',
                                 domain="[('room_id','=',room_id)]")
    leave_request_id = fields.Many2one(comodel_name='leave_request')
    start_date = fields.Date(related='leave_request_id.leave_date',readonly=False)
    arrival_date = fields.Date(related = 'leave_request_id.arrival_date',readonly=False)


    def generate_report_pdf(self):
        """While clicking button need to generate PDF report"""
        self.ensure_one()
        return self.leave_request_report()

    def leave_request_report(self):
        query = """ select hr.room_number,st.student_name,
        lr.leave_date,lr.arrival_date from hostel_room as hr 
        inner join student_details as st on hr.id = st.room_id
        inner join leave_request as lr on st.id = lr.student_id"""

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data = {'report':report}
        print(data)
        return self.env.ref('hostel_management.leave_request_report'
                            ).report_action(None,data=data)





