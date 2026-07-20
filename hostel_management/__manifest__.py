# -*- coding: utf-8 -*-
{
    'name': "Hostel Management",
    'version': "19.0.1.0",
    'liscense': "LGPL-3",
    'author': "faris",
    'category': "hostel management",
    'summary': """an erp for hostel management""",
    'description': """an complete module for an hostel management""",
    'sequence': 1,
    'application': True,
    'installable': True,
    'auto_install': True,
    'depends': ['mail', 'sale_management', 'account', 'base_automation'],
    'data': [
        "security/hostel_management_groups.xml",
        "security/company_record.xml",
        "security/ir.model.access.csv",
        "data/user_cron_data.xml",
        "data/ir_cron_data.xml",
        "data/rental_product.xml",
        "data/sequence_data.xml",
        "report/hostel_management_report.xml",
        "report/hostel_student_report.xml",
        "wizard/student_report_view.xml",
        "views/hostel_cleaning.xml",
        "views/hostel_email_template.xml",
        "views/hostel_inherit_account_move.xml",
        "views/hostel_leave_views.xml",
        "views/hostel_room_views.xml",
        "views/hostel_student_views.xml",
        "views/hostel_facilities.xml",
        "views/hostel_menu_views.xml"],

    'demo': [
        "demo/demo.xml",
    ]
}
