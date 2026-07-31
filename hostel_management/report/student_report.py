# -*- coding:utf-8 -*-
import io

from odoo import models, api

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class StudentReport(models.AbstractModel):
    """created as an abstract model it won't store anything in
    the database its connect the ir.action report model"""
    _name = 'report.hostel_management.student_report'
    _description = 'Report Created'

    @api.model
    def _get_report_values(self, docids, data=None):
        """This is  standard method to call the datas from the transient
                model and return the values into dictionary"""
        room = self.env['hostel.room'].browse(data['room_number'])
        student = self.env['student.details'].browse(data['student_name'])
        return {
            'doc_ids': docids,
            'doc_model': 'student.report.wizard',
            'data': data['report'],
            'room_number': room,
            'student_name': student
        }

    def get_xlsx_report(self, data, response):
        """This is function used to create excel report it will return
         values in dictionary """
        output = io.BytesIO()
        print('this is what when BytesIo prints', output)
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Student Report')
        sheet.set_column(1, 1, 15)
        sheet.set_column(2, 2, 15)
        border = workbook.add_format({'border': 1})
        # green = workbook.add_format({'bg_color': '#28A828', 'border': 1})
        # red = workbook.add_format({'bg_color': '#ff3333', 'border': 1})
        # rose = workbook.add_format({'bg_color': '#DA70D6', 'border': 1})
        head = workbook.add_format(
            {'bold': True, 'font_size': 30, 'align': 'center'})
        sheet.merge_range('C3:K6', 'Student Report', head)
        sheet.merge_range('B8:C9', 'Student Name: ' + data['student_name'])
        sheet.merge_range('B10:C11', 'Pending Amount: ' + data['pending_amount'])
        sheet.merge_range('C12:D13', 'Room : ' + data['room_number'])
        sheet.merge_range('D14:E15', 'Invoice Status: ' + data['invoice_status'])
        sheet.merge_range('B16:B17', 'Sl.No', border)
        sheet.merge_range('C16:C17', 'Name', border)
        sheet.merge_range('D16:D17', 'Pending_amount', border)
        sheet.merge_range('E16:E17','Room', border)
        sheet.merge_range('F16:F17', 'Invoice Status', border)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()


