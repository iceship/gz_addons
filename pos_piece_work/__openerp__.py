# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': '用POS的方式做计件输入',
    'version': '0.1',
    'category': 'Wages',
    'description': """
用POS的方式做计件输入。
=======================================================================================
用POS的方式做计件输入。
""",
    'author': 'Wang Yue Ming',
    'website': 'http://openerp.com',
    'depends': ['piece_rate', 'hr_factory'],
    'data': [
        'views/pos_piece_work.xml',
    ],
    'qweb': [
        'static/src/xml/pos_pw.xml',
    ],
    'demo': [],
    'test':[],
    'installable': True,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
