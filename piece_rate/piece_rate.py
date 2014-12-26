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
import logging

_logger = logging.getLogger(__name__)

#----------------------------------------------------------
# 工序
#----------------------------------------------------------
class work_procedure(osv.osv):
    _name = 'work.procedure'

    _columns = {
        'name': fields.char(u'名称', required=True, select=True),
    }
    _sql_constraints = [
        ('name', 'unique(name)', u'工序名称不能重复'),
    ]
    _order = 'name'
    
#----------------------------------------------------------
# 款号
#----------------------------------------------------------
class style_no(osv.osv):
    _name = 'style.no'

    _columns = {
        'name': fields.char(u'名称', required=True, select=True),
        'rate_ids': fields.one2many('piece.rate', 'style_id', u'工价'),
    }
    _sql_constraints = [
        ('name', 'unique(name)', u'款号名称不能重复'),
    ]
    _order = 'name'
    
#----------------------------------------------------------
# 计件工价
#----------------------------------------------------------
class piece_rate(osv.osv):
    _name = 'piece.rate'

    _columns = {
        'style_id': fields.many2one('style.no', u'款号', required=True, select=True),
        'procedure': fields.many2one('work.procedure', u'工序', required=True, select=True),
        'rate': fields.float(u'工价', digits=(7,3), required=True),
    }
    _sql_constraints = [
        ('procedure', 'unique(style_id, procedure)', u'同款号工序不能重复'),
    ]
    _order = 'style_id, procedure'
