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
# 员工管理
#----------------------------------------------------------
class hr_employee(osv.osv):
    _inherit = 'hr.employee'

    _columns = {
        'emp_id': fields.char(u'工号', required=True, select=True),
        'procedure': fields.many2one('work.procedure', u'默认工序', required=True, select=True),
        'entry_day': fields.date(u'入职日期'),
        'quit_day': fields.date(u'离职日期'),
    }
    _sql_constraints = [
        ('emp_id', 'unique(emp_id)', u'工号不能重复'),
    ]
    
    def _check_emp_id(self, cr, uid, ids):
        for record in self.browse(cr, uid, ids):
            if not _validating_number(record.emp_id): 
                return False
        return True

    _constraints = [
        (_check_emp_id, u'工号必须是数字', ['emp_id']),
    ]
