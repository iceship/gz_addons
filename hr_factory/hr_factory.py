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
import re
import logging

_logger = logging.getLogger(__name__)

def _validating_number(num):
    return re.match(r"^[0-9]+$", num) != None

#----------------------------------------------------------
# 车间
#----------------------------------------------------------
class hr_workshop(osv.osv):
    _name = "hr.workshop"
    
    _columns = {
        'name': fields.char(u'车间', required=True),
        'workline_ids': fields.one2many('hr.workline', 'workshop_id', u'组别'),
        'manager_id': fields.many2one('hr.employee', u'经理'),
        'note': fields.text(u'备注'),
    }

#----------------------------------------------------------
# 组别
#----------------------------------------------------------
class hr_workline(osv.osv):
    _name = "hr.workline"
    
    def _dept_name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _columns = {
        'name': fields.char(u'组别', required=True),
        'complete_name': fields.function(_dept_name_get_fnc, type="char", string=u'组别'),
        'workshop_id': fields.many2one('hr.workshop', u'车间', ondelete='cascade', required=True, select=True),
        'manager_id': fields.many2one('hr.employee', u'组长'),
        'note': fields.text(u'备注'),
    }

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if not ids:
            return []
        workshop_pool = self.pool.get('hr.workshop')
        reads = self.read(cr, uid, ids, ['name','workshop_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['workshop_id']:
                workshop = workshop_pool.read(cr, uid, [record['workshop_id'][0]], ['name'], context=context)
                name = workshop[0]['name'] + ' / ' + name
            res.append((record['id'], name))
        return res

#----------------------------------------------------------
# 员工管理
#----------------------------------------------------------
class hr_employee(osv.osv):
    _inherit = 'hr.employee'

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if not ids:
            return []
        reads = self.read(cr, uid, ids, ['name','emp_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['emp_id']:
                name = record['emp_id'] + ' ' + name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if args is None:
            args = []
        if name:
            ids = self.search(cr, user, ['|',('emp_id', operator, name),('name', operator, name)] + args, limit=limit)
            return self.name_get(cr, user, ids, context=context)
        return super(hr_employee, self).name_search(cr, user, name, args=args, operator=operator, context=context, limit=limit)
        
    _columns = {
        'emp_id': fields.char(u'工号', required=True, select=True),
        'workshop_id': fields.many2one('hr.workshop', u'车间', select=True),
        'workline_id': fields.many2one('hr.workline', u'组别', domain="[('workshop_id','=',workshop_id)]", select=True),
        'procedure_id': fields.many2one('work.procedure', u'默认工序', required=True, select=True),
        'entry_day': fields.date(u'入职日期'),
        'quit_day': fields.date(u'离职日期'),
    }
    _sql_constraints = [
        ('emp_id', 'unique(emp_id)', u'工号不能重复'),
    ]
    _order = 'emp_id, name_related'
    
    def onchange_workshop_id(self, cr, uid, ids, workshop_id, context=None):
        if workshop_id:
            return {'value': {'workline_id': False}}
        return {'value': {}}

    def _check_emp_id(self, cr, uid, ids):
        for record in self.browse(cr, uid, ids):
            if not _validating_number(record.emp_id): 
                return False
        return True

    _constraints = [
        (_check_emp_id, u'工号必须是数字', ['emp_id']),
    ]
