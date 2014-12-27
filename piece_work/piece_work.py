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

from openerp.osv import osv
from openerp.osv import fields
import openerp.addons.decimal_precision as dp
import time
import logging

_logger = logging.getLogger(__name__)

#----------------------------------------------------------
# 计件计量
#----------------------------------------------------------
class piece_work_line(osv.osv):
    _name = 'piece.work.line'

    _columns = {
        'emp_id': fields.many2one('hr.employee', u'工号', required=True, select=True),
        'style_id': fields.many2one('style.no', u'款号', required=True, select=True),
        'rate_id': fields.many2one('piece.rate', u'工序', required=True, select=True),
        'unit_qty': fields.float(u'数量', digits_compute= dp.get_precision('Product Unit of Measure'), required=True),
        'uom_id': fields.many2one('product.uom', u'计量单位', required=True),
        'date': fields.date(u'日期', required=True, select=True, copy=False),
        'hours': fields.float(u'工时', digits=(4,2)),
        'is_extrahours': fields.boolean(u'是否为突击性工作', select=True),
        'description': fields.text(u'备注'),
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'hours': 9,
    }
    _order = 'date desc, emp_id'