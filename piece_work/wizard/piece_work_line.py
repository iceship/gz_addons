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

from openerp.osv import fields, osv
import datetime
import time

class wizard_piece_work_line(osv.osv_memory):
    _name = 'wizard.piece.work.line'
    
    _columns = {
        'date_from': fields.date('From', required=True),
        'date_to': fields.date('To', required=True),
        'emp_id': fields.many2one('hr.employee', u'工号'),
        'style_id': fields.many2one('style.no', u'款号'),
        'rate_id': fields.many2one('piece.rate', u'工序', domain="[('style_id','=',style_id)]"),
    }

    def _date_from(*a):
        return datetime.date.today().replace(day=1).strftime('%Y-%m-%d')

    def _date_to(*a):
        return datetime.date.today().strftime('%Y-%m-%d')

    _defaults = {
        'date_from': _date_from,
        'date_to': _date_to
    }

    def retrieve_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)[0]
        
        domain = [('date','>=',data['date_from']),('date','<=',data['date_to'])]
        if data['emp_id']:
            domain += [('emp_id','=',data['emp_id'][0])]
        if data['style_id']:
            domain += [('style_id','=',data['style_id'][0])]
        if data['rate_id']:
            domain += [('rate_id','=',data['rate_id'][0])]

        return {
            'domain': str(domain),
            'name': u'所有记录',
            'view_type': 'form',
            'view_mode': 'graph,tree',
            'res_model': 'piece.work.line',
            'type': 'ir.actions.act_window',
        }
