# -*- coding: utf-8 -*-
import json
import io
from time import strftime

from odoo import models, fields
from odoo.tools import json_default
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class LeaveRequestWizard(models.TransientModel):
    """Class that is to store values for leave request wizard created
    as  transient model"""
    _name = 'leave.request.report.wizard'

    room_ids = fields.Many2many(comodel_name='hostel.room')
    student_ids = fields.Many2many(comodel_name='student.details',
                                  domain="[('room_id','=',room_ids)]")
    start_date = fields.Date(string='Start Date')
    arrival_date = fields.Date(string='Arrival Date')

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

        if self.student_ids:
            query += """ and st.id in %s """
            params.append(tuple(self.student_ids.ids))

        if self.start_date :
            query += """ and lr.leave_date >= %s """
            params.append(self.start_date)

        if self.arrival_date :
            query += """ and lr.arrival_date <= %s """
            params.append(self.arrival_date)


        self.env.cr.execute(query,params)
        report = self.env.cr.dictfetchall()
        data = {'student_name': self.student_ids.ids,
                'room_number': self.room_ids.ids,
                'start_date': self.start_date,
                'arrival_date': self.arrival_date,
                'report': report}
        print("This is the data passing from transient model",data)
        return self.env.ref('hostel_management.action_leave_report'
                            ).report_action(None, data=data)

    def generate_excel_report(self):
        datas={
            'room_number': self.room_ids.ids,
            'student_name': self.student_ids.ids,
        }
        return{
            'type' : 'ir.actions.report',
            'data' : {'model' : 'leave.request.report.wizard',
                      'options':json.dumps(datas,default=json_default),
                      'output_format':'xlsx',
                      'report_name': 'Leave report'},
            'report_type': 'xlsx'

        }

    def get_xlsx_report(self,datas,response):
        query = """ select hr.id as room_id,st.id as student_id,st.student_name,
                lr.leave_date,lr.arrival_date,hr.room_number,
                lr.arrival_date-lr.leave_date as Duration from hostel_room as hr 
                inner join student_details as st on hr.id = st.room_id
                inner join leave_request as lr on lr.student_id = st.id where 1=1   """

        params = []

        if datas['room_number']:
            query += """ and hr.id in %s """
            params.append(tuple(datas['room_number']))

        if datas['student_name']:
            query += """ and st.id in %s """
            params.append(tuple(datas['student_name']))

        if self.start_date:
            query += """ and lr.leave_date >= %s """
            params.append(self.start_date)

        if self.arrival_date:
            query += """ and lr.arrival_date <= %s """
            params.append(self.arrival_date)

        self.env.cr.execute(query, params)
        report = self.env.cr.dictfetchall()
        print('data fetched from sql query',report)

        room=self.env['hostel.room'].browse(datas['room_number'])
        student=self.env['student.details'].browse(datas['student_name'])

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output,{'in_memory': True})
        sheet = workbook.add_worksheet()
        sheet.set_column(4, 10, 20)
        sheet.set_row(0, 50)
        border = workbook.add_format({'border': 1, 'align': 'center'})
        text = workbook.add_format({'align': 'center', 'border': 1})
        head = workbook.add_format(
            {'bold': True, 'font_size': 20, 'align': 'center'})
        sheet.merge_range('D1:H1', 'Leave Report', head)
        if room:
            a=[]
            for rec in room:
                a.append(rec.room_number)
            sheet.merge_range('D2:H2','Rooms:'+','.join(a))

        if student:
            b=[]
            for rec in student:
                b.append(rec.student_name)
            sheet.merge_range('D3:H3','Students:'+','.join(b))


        sheet.write('D4', 'Sl.No', border)
        sheet.write('E4', 'Student Name', border)
        sheet.write('F4', 'Room Number', border)
        sheet.write('G4', 'Start Date', border)
        sheet.write('H4', 'Arrival Date', border)
        sheet.write('I4', 'Duration', border)

        row=4
        number=0

        for new in report:
            number+=1
            print(new['leave_date'].strftime('%y-%m-%-d'))
            sheet.write(row, 3,number,text)
            sheet.write(row, 4 , new['student_name'],text)
            sheet.write(row, 5, new['room_number'],text)
            sheet.write(row, 6, new['leave_date'].strftime('%y-%m-%d'),text)
            sheet.write(row, 7,new['arrival_date'].strftime('%y-%m-%d'),text)
            sheet.write(row, 8, new['duration'],text)

            row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()







