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

    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.rate_id.rate * line.unit_qty
        return res

    _columns = {
        'type': fields.selection([
            ('normal', u'正常'),
            ('rework', u'返工'),
            ('scrap', u'报废'),
            ], u'类型', required=True, select=True),
        'emp_id': fields.many2one('hr.employee', u'工号', required=True, select=True),
        'workline_id': fields.related('emp_id', 'workline_id', type='many2one', relation='hr.workline', string=u'组别', readonly="1"),
        'style_id': fields.many2one('style.no', u'款号', required=True, select=True),
        'rate_id': fields.many2one('piece.rate', u'工序', domain="[('style_id','=',style_id)]", required=True, select=True),
        'unit_qty': fields.float(u'数量', digits_compute= dp.get_precision('Product Unit of Measure'), required=True),
        'uom_id': fields.many2one('product.uom', u'计量单位', required=True),
        'wage_subtotal': fields.function(_amount_line, string=u'小计', digits_compute= dp.get_precision('Account'), store=True),
        'date': fields.date(u'日期', required=True, select=True, copy=False),
        'hours': fields.float(u'工时', digits=(4,2)),
        'is_extrahours': fields.boolean(u'是否为突击性工作', select=True),
        'lock_style': fields.boolean(u'锁定款号'),
        'description': fields.text(u'备注'),
        'state': fields.selection([
            ('draft', u'录入'),
            ('confirm', '已确认'),
            ], u'状态', readonly=True, copy=False, select=True),
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'lock_style': lambda self, cr, uid, context: self.pool.get('user.param').read_bool(cr, uid, self._name, 'lock_style'),
        'style_id': lambda self, cr, uid, context: self.pool.get('user.param').read_bool(cr, uid, self._name, 'lock_style') and self.pool.get('user.param').read_int(cr, uid, self._name, 'style_id') or False,
        'hours': 9,
        'state': 'draft',
    }
    _order = 'date desc, emp_id'
    
    def onchange_emp_id(self, cr, uid, ids, emp_id, style_id, context=None):
        if emp_id:
            employee = self.pool.get('hr.employee').browse(cr, uid, emp_id, context=context)
            res = {'value': {'workline_id': employee.workline_id and employee.workline_id.id or False}}
            if style_id:
                rate_id = self.pool.get('piece.rate').search(cr, uid, [('style_id', '=', style_id),('procedure_id', '=', employee.procedure_id.id)], context=context)
                if rate_id:
                    res['value']['rate_id'] = rate_id[0]
                else:
                    res['value']['rate_id'] = False
            return res
            
        return {'value': {}}

    def onchange_style_id(self, cr, uid, ids, emp_id, style_id, context=None):
        if style_id and emp_id:
            employee = self.pool.get('hr.employee').browse(cr, uid, emp_id, context=context)
            rate_id = self.pool.get('piece.rate').search(cr, uid, [('style_id', '=', style_id),('procedure_id', '=', employee.procedure_id.id)], context=context)
            if rate_id:
                return {'value': {'rate_id': rate_id[0]}}
            else:
                return {'value': {'rate_id': False}}
            
        return {'value': {}}
    
    def onchange_rate_id(self, cr, uid, ids, rate_id, context=None):
        if rate_id:
            rate = self.pool.get('piece.rate').browse(cr, uid, rate_id, context=context)
            return {'value': {'uom_id': rate.procedure_uom.id}}
        return {'value': {}}

    def unlink(self, cr, uid, ids, context=None):
        return super(piece_work_line, self).unlink(cr, uid, ids, context=context)
        
    def _save_lock_style(self, cr, uid, id, context=None):
        line = self.browse(cr, uid, id)
        user_param = self.pool.get('user.param')
        user_param.write_bool(cr, uid, self._name, 'lock_style', line.lock_style)
        if line.lock_style:
            user_param.write_int(cr, uid, self._name, 'style_id', line.style_id.id)
        
    def create(self, cr, uid, vals, context=None):
        new_id = super(piece_work_line, self).create(cr, uid, vals, context=context)
        self._save_lock_style(cr, uid, new_id)
        return new_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(piece_work_line, self).write(cr, uid, ids, vals, context=context)
        self._save_lock_style(cr, uid, ids[0])
        return res
