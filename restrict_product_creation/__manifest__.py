#-*- coding: utf-8 -*-
{
    "name": "Restrict Product Creation",
    "summary": "Restrict Product Creation for users",
    "version": "19.0.1.0.0",
    "description": "Users can’t create products directly; they submit a “New Item Request” that a Manager approves to auto-create product.",
    "license":'LGPL-3',
    "author":"faris",
    "installable":True,
    "application":True,
    "sequence":4,
    "depends":['base','sale_management'],
    "data":[
        "security/product_template_groups.xml",
        "security/ir.model.access.csv",
        "views/new_item_request_views.xml",
        "views/restrict_product_creation_menu.xml"

    ]

}