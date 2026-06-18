# -*- coding: utf-8 -*-
{
    'name': "Hostel Management",
    'version':"19.0.1.0",
    'liscense': "LGPL-3",
    'author':"faris",
    'category':"hostel management",
    'summary':"""an erp for hostel management""",
    'description':"""an complete module for an hostel management""",
    'sequence':1,
    'application':True,
    'installable':True,
    # 'auto_install':True,
    'depends':['mail'],
    'data':[
        "security/ir.model.access.csv",
        "views/hostel_room_views.xml",
        "views/hostel_student_views.xml",
        "views/hostel_menu_views.xml"]


}
