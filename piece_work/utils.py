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

class user_param(osv.osv):
    _name = 'user.param'
    
    _columns = {
        'res_model': fields.char('Resource Model'),
        'name': fields.char('Name'),
        'char_value': fields.char('Char Value'),
        'bool_value': fields.boolean('Boolean Value'),
        'int_value': fields.integer('Integer Value'),
        'uid': fields.many2one('res.users', u'owner'),
    }
    
    def write_bool(self, cr, uid, res_model, name, value):
        ids = self.search(cr, uid, [('uid','=',uid),('res_model','=',res_model),('name','=',name)])
        if ids:
            self.write(cr, uid, ids, {'bool_value': value})
        else:
            self.create(cr, uid, {'uid':uid, 'res_model':res_model, 'name':name, 'bool_value':value})
            
    def read_bool(self, cr, uid, res_model, name):
        ids = self.search(cr, uid, [('uid','=',uid),('res_model','=',res_model),('name','=',name)])
        if ids:
            return self.read(cr, uid, ids, ['bool_value'])[0]['bool_value']

        return False

    def write_int(self, cr, uid, res_model, name, value):
        ids = self.search(cr, uid, [('uid','=',uid),('res_model','=',res_model),('name','=',name)])
        if ids:
            self.write(cr, uid, ids, {'int_value': value})
        else:
            self.create(cr, uid, {'uid':uid, 'res_model':res_model, 'name':name, 'int_value':value})
            
    def read_int(self, cr, uid, res_model, name):
        ids = self.search(cr, uid, [('uid','=',uid),('res_model','=',res_model),('name','=',name)])
        if ids:
            return self.read(cr, uid, ids, ['int_value'])[0]['int_value']

        return 0
