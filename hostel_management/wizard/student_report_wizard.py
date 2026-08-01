# -*- coding: utf-8 -*-
import json
import io
from odoo import models, fields
from odoo.tools import json_default
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter



class StudentReportWizard(models.TransientModel):
    """class that is to store values for student report wizard
    created as  transient model """
    _name = 'student.report.wizard'
    _description = 'Student report have been created'

    room_ids = fields.Many2many(comodel_name='hostel.room')
    student_ids = fields.Many2many(comodel_name='student.details',
                                 domain = "[('room_id', '=', room_ids)]")


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
        from hostel_room as hr inner join student_details as st on hr.id = st.room_id left join account_move as am on am.student_id = st.id where 1=1"""

        params = []

        if self.room_ids:
            query += """ and hr.id in %s"""
            params.append(tuple(self.room_ids.ids))

        if self.student_ids:
            query += """ and st.id in %s"""
            params.append(tuple(self.student_ids.ids))

        query += """ group by hr.id,st.id"""



        self.env.cr.execute(query,params)
        report = self.env.cr.dictfetchall()


        data =  {'room_number':self.room_ids.ids,
                 'student_name':self.student_ids.ids,
                 'report': report}
        return self.env.ref('hostel_management.action_student_report'
                            ).report_action(None,data=data)


    def generate_excel(self):
        ''' This function work while clicking the EXCEL report button and this will redirect to another function '''
        data = {
            'room_number':self.room_ids.ids,
            'student_name':self.student_ids.ids,
        }
        print('this is the data passed through wizard while clicking button',data)
        return{
            'type' : 'ir.actions.report',
            'data' : {'model' : 'student.report.wizard',
                      'options':json.dumps(data,default=json_default),
                      'output_format':'xlsx',
                      'report_name': 'Students report'},
            'report_type': 'xlsx'

        }


    def get_xlsx_report(self,data,response):
        """linked with action report it helps to sort the datas inside
        the table and this will pass the values into PDF"""
        query = """ select hr.id as room_id,st.id as student_id,
        hr.room_number,SUM(am.amount_residual)as pending_amount,
        st.student_name,case when(SUM(am.amount_residual)>0) then 'pending' else  'done' end as invoice_status
        from hostel_room as hr inner join student_details as st on hr.id = st.room_id left join account_move as am on am.student_id = st.id where 1=1"""

        params = []

        if self.room_ids:
            query += """ and hr.id in %s"""
            params.append(tuple(self.room_ids.ids))

        if self.student_ids:
            query += """ and st.id in %s"""
            params.append(tuple(self.student_ids.ids))

        query += """ group by hr.id,st.id"""



        self.env.cr.execute(query,params)
        report = self.env.cr.dictfetchall()

        print('this dictionary contains values of query', report)
        room = self.browse(data['room_number'])
        student = self.browse(data['student_name'])
        print('this is the recordset passed from wizard',room)
        print('this is the recordset passed from wizard',student)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output,{'in_memory':True})
        sheet = workbook.add_worksheet()
        sheet.set_column(8,10,20)
        sheet.set_column(4,10,20)
        border = workbook.add_format({'border': 1,})
        head = workbook.add_format(
            {'bold': True, 'font_size': 30, 'align': 'center'})
        sheet.write('F8', 'Student Report' , head)
        sheet.write('D10', 'Sl.No', border)
        sheet.write('E10', 'Student Name', border)
        sheet.write('F10', 'Pending Amount', border)
        sheet.write('G10', 'Room Number', border)
        sheet.write('H10', 'Invoice Status', border)

        row=11
        col = 5

        for new in report:
            col+=1
            print('this is the dictionary inside the loop',new)
            sheet.write('E11', new['student_name'])
            sheet.write('F11', new['pending_amount'])
            sheet.write('G11', new['room_number'])
            sheet.write('H11',new['invoice_status'])


        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()





