# -*- coding: utf-8 -*-
from odoo import models, fields


class LeaveRequestWizard(models.TransientModel):
    """Class that is to store values for leave request wizard created
    as  transient model"""
    _name = 'leave.request.report.wizard'

    room_id = fields.Many2one(comodel_name='hostel.room')
    student_id = fields.Many2many(comodel_name='student.details',
                                  domain="[('room_id','=',room_id)]")
    start_date = fields.Date(string='Start Date')
    arrival_date = fields.Date(string='Arrival Date')
    student_name = fields.Char(related='student_id.student_name',
                               string='Student Name')
    room_number = fields.Char(related='room_id.room_number',
                              string='Room Number')

    def generate_report_pdf(self):
        """While clicking button need to generate PDF report"""
        self.ensure_one()
        return self.action_leave_report()

    def action_leave_report(self):
        query = """ select hr.room_number,st.student_name,lr.start_date,lr.arrival_date,lr.arrival_date-lr.start_date as Duration from hostel_room as hr 
        inner join student_details as st on hr.id = st.room_id
        inner join leave_request_report_wizard as lr on hr.id = lr.room_id """

        if self.student_id:
            query += """ where st.id in %s """

        # if self.start_date and self.arrival_date:
        #     query += """ between '%s' and '%s' """

        self.env.cr.execute(query, (tuple(self.student_id.ids),))
        report = self.env.cr.dictfetchall()
        data = {'student_name': self.student_name,
                'room_number': self.room_number,
                'start_date': self.start_date,
                'arrival_date': self.arrival_date, 'report': report}
        print('data fetched from sql', data)
        return self.env.ref('hostel_management.action_leave_report'
                            ).report_action(None, data=data)
