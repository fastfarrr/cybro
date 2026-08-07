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
        datas = {
            'room_number':self.room_ids.ids,
            'student_name':self.student_ids.ids,
        }
        print('this is the data passed through wizard while clicking button',datas)
        return{
            'type' : 'ir.actions.report',
            'data' : {'model' : 'student.report.wizard',
                      'options':json.dumps(datas,default=json_default),
                      'output_format':'xlsx',
                      'report_name': 'Students report'},
            'report_type': 'xlsx'

        }


    def get_xlsx_report(self,datas,response):

        """linked with action report it helps to sort the datas inside
        the table and this will pass the values into PDF"""
        query = """ select hr.id as room_id,st.id as student_id,
                hr.room_number,SUM(am.amount_residual)as pending_amount,
                st.student_name,case when(SUM(am.amount_residual)>0) then 'pending' else  'done' end as invoice_status
                from hostel_room as hr inner join student_details as st on hr.id = st.room_id left join account_move as am on am.student_id = st.id where 1=1"""

        new_params = []

        if datas['room_number']:
            # room_number=datas.env['hostel.room'].browse(datas['room_number'])
            print('room_number ids',datas['room_number'])
            query += """ and hr.id in %s """
            new_params.append(tuple(datas['room_number']))

        if datas['student_name']:
            query += """ and st.id in %s """
            new_params.append(tuple(datas['student_name']))

        query += """ group by hr.id,st.id"""
        print(123123, self)
        self.env.cr.execute(query, new_params)
        report = self.env.cr.dictfetchall()

        print('this dictionary contains values of query', report)
        room = self.env['hostel.room'].browse(datas['room_number'])

        student = self.env['student.details'].browse(datas['student_name'])

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output,{'in_memory':True})
        sheet = workbook.add_worksheet()
        sheet.set_column(4,10,20)
        sheet.set_row(0,50)
        border = workbook.add_format({'border': 1, 'align': 'center','bg_color':'blue'})
        text = workbook.add_format({'align':'center','border':1})
        head = workbook.add_format(
            {'bold': True, 'font_size': 20, 'align': 'center'})
        sheet.merge_range('D1:H1', 'Student Report' , head)

        if student:
            a=[]
            for rec in student:
                a.append(rec.student_name)
            print('this is the list',a)
            sheet.merge_range('D2:H2',"students:" + ','.join(a))
        if room:
            b=[]
            for rec in room:
                b.append(rec.room_number)
            print('this is the list',b)
            sheet.merge_range('D3:H3','Rooms:' + ','.join(b))


        sheet.write('D4', 'Sl.No', border)
        sheet.write('E4', 'Student Name', border)
        sheet.write('F4', 'Pending Amount', border)
        sheet.write('G4', 'Room Number', border)
        sheet.write('H4', 'Invoice Status', border)


        row=4
        number=0
        for new in report:
            number +=1
            print('this is the dictionary inside the loop',new)
            sheet.write(row,3,number,text)
            sheet.write(row,4,new['student_name'],text)
            sheet.write(row,5,new['pending_amount'],text)
            sheet.write(row,6,new['room_number'],text)
            sheet.write(row,7,new['invoice_status'],text)
            row += 1






        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()





