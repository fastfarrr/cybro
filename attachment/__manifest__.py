# # -*- coding: utf-8 -*-
{
    'name': 'purchase order attachment',
    'version':'19.0.1.0',
    'author':'faris',
    'summary':'Checks is any file attatched on purchase order',
    'lisence':'LGPL-3',
    'installable':True,
    'application':True,
    'auto_install':True,
    'sequence':3,
    'depends':['purchase'],
    'data':[
        'views/res_config_settings.xml'
    ]
}