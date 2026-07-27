# -*- coding: utf-8 -*-
from odoo import models,api
class LeaveRequestReport(models.AbstractModel):
    """An abstract model to return the PDF values that comes from the transient model"""
    _name = "report.hostel_management.leave_report"

    @api.model
    def _get_report_values(self,docids,data=None):
        """This is  standard method to call the datas from the transient
        model and return the values into dictionary"""
        print("this is the data is passing from the abstract model",data)


        return{
            'doc_ids' : docids,
            'doc_model' : 'leave.request.report.wizard',
            'data' : data['report'],
            'room_number' : data['room_number'],
            'student_name' : data['student_name'],
            'start_date' : data['start_date'],
            'arrival_date' : data['arrival_date'],
        }


