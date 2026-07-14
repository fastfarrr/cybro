# -*- coding: utf-8 -*-
{
    "name": "Vendor Product List",
    "version": "19.0.1.0.0",
    "author": "faris",
    "license": "LGPL-3",
    "summary": "Vendor Product List",
    "description": "There will be an extra selectable button in purchase order if its clicked it will show every product selected in vendor",
    "installable": True,
    "sequence": 4,
    "application": True,
    "depends": ['base','purchase'],
    "data": {
        "views/vendor_product_list_vendor_list.xml"

    }
}
