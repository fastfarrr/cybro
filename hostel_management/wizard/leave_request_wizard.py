# -*- coding: utf-8 -*-
from odoo import models, fields


class LeaveRequestWizard(models.TransientModel):
    """Class that is to store values for leave request wizard created
    as  transient model"""
    _name = 'leave.request.report.wizard'

    room_ids = fields.Many2many(comodel_name='hostel.room')
    student_ids = fields.Many2many(comodel_name='student.details',
                                  domain="[('room_id','=',room_ids)]")
    start_date = fields.Date(string='Start Date')
    arrival_date = fields.Date(string='Arrival Date')
    student_name = fields.Char(related='student_ids.student_name',
                               string='Student Name')
    room_number = fields.Char(related='room_ids.room_number',
                              string='Room Number')

    def generate_report_pdf(self):
        """While clicking button need to generate PDF report"""
        self.ensure_one()
        return self.action_leave_report()

    def action_leave_report(self):
        """This method will execute when the button is clicked, to generate
         PDF and this passes the psql query that needed for our PDF generation"""

        query = """ select hr.id as room_id,st.id as student_id,st.student_name,
        lr.leave_date,lr.arrival_date,hr.room_number,
        lr.arrival_date-lr.leave_date as Duration from hostel_room as hr 
        inner join student_details as st on hr.id = st.room_id
        inner join leave_request as lr on lr.student_id = st.id where 1=1   """

        params=[]

        if self.room_ids:
            query += """ and hr.id in %s """
            params.append(tuple(self.room_ids.ids))
            print("this param when u select room",params)

        if self.student_ids:
            query += """ and st.id in %s """
            params.append(tuple(self.student_ids.ids))
            print("this param when u select student",params)
        #
        # if self.start_date and self.arrival_date:
        #     query += """ and lr.leave_date between %s and %s """
        #     params.append(self.start_date)


        self.env.cr.execute(query,params)
        report = self.env.cr.dictfetchall()
        data = {'student_name': self.student_name,
                'room_number': self.room_number,
                'start_date': self.start_date,
                'arrival_date': self.arrival_date,
                'report': report}
        print("This is the data passing from transient model",data)
        return self.env.ref('hostel_management.action_leave_report'
                            ).report_action(None, data=data)
