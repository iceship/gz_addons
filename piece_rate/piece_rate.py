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
import logging

_logger = logging.getLogger(__name__)

#----------------------------------------------------------
# 工序
#----------------------------------------------------------
class work_procedure(osv.osv):
    _name = 'work.procedure'
    _inherits = {'product.template': 'product_tmpl_id'}
    _inherit = ['mail.thread']

    def _get_uom_id(self, cr, uid, *args):
        return self.pool.get('ir.model.data').get_object_reference(cr, uid, 'product', 'product_uom_dozen')[1]

    _columns = {
        'product_tmpl_id': fields.many2one('product.template', 'Product Template', required=True, ondelete="cascade", select=True, auto_join=True),
    }
    #_sql_constraints = [
    #    ('name', 'unique(name)', u'工序名称不能重复'),
    #]

    _defaults = {
        'sale_ok': 0,
        'uom_id': _get_uom_id,
        'uom_po_id': _get_uom_id,
        'categ_id' : False,
        'type' : 'service',
    }
    
    def unlink(self, cr, uid, ids, context=None):
        unlink_ids = []
        unlink_product_tmpl_ids = []
        for product in self.browse(cr, uid, ids, context=context):
            # Check if product still exists, in case it has been unlinked by unlinking its template
            if not product.exists():
                continue
            tmpl_id = product.product_tmpl_id.id
            # Check if the product is last product of this template
            other_product_ids = self.search(cr, uid, [('product_tmpl_id', '=', tmpl_id), ('id', '!=', product.id)], context=context)
            if not other_product_ids:
                unlink_product_tmpl_ids.append(tmpl_id)
            unlink_ids.append(product.id)
        res = super(work_procedure, self).unlink(cr, uid, unlink_ids, context=context)
        # delete templates after calling super, as deleting template could lead to deleting
        # products due to ondelete='cascade'
        self.pool.get('product.template').unlink(cr, uid, unlink_product_tmpl_ids, context=context)
        return res
        
    def onchange_uom(self, cursor, user, ids, uom_id, uom_po_id):
        if uom_id:
            return {'value': {'uom_po_id': uom_id}}
        return {}
    
#----------------------------------------------------------
# 款号
#----------------------------------------------------------
class style_no(osv.osv):
    _name = 'style.no'
    _inherits = {'product.template': 'product_tmpl_id'}
    _inherit = ['mail.thread']

    def _get_uom_id(self, cr, uid, *args):
        return self.pool.get('ir.model.data').get_object_reference(cr, uid, 'product', 'product_uom_dozen')[1]
        
    def _default_category(self, cr, uid, context=None):
        return self.pool.get('ir.model.data').get_object_reference(cr, uid, 'piece_rate', 'prod_cat_service')[1]
        
    _columns = {
        'product_tmpl_id': fields.many2one('product.template', 'Product Template', required=True, ondelete="cascade", select=True, auto_join=True),
        'rate_ids': fields.one2many('piece.rate', 'style_id', u'工价'),
    }
    #_sql_constraints = [
    #    ('name', 'unique(name)', u'款号名称不能重复'),
    #]
    _defaults = {
        'sale_ok': 0,
        'uom_id': _get_uom_id,
        'uom_po_id': _get_uom_id,
        'categ_id' : _default_category,
        'type' : 'service',
    }
    
    def unlink(self, cr, uid, ids, context=None):
        unlink_ids = []
        unlink_product_tmpl_ids = []
        for product in self.browse(cr, uid, ids, context=context):
            # Check if product still exists, in case it has been unlinked by unlinking its template
            if not product.exists():
                continue
            tmpl_id = product.product_tmpl_id.id
            # Check if the product is last product of this template
            other_product_ids = self.search(cr, uid, [('product_tmpl_id', '=', tmpl_id), ('id', '!=', product.id)], context=context)
            if not other_product_ids:
                unlink_product_tmpl_ids.append(tmpl_id)
            unlink_ids.append(product.id)
        res = super(style_no, self).unlink(cr, uid, unlink_ids, context=context)
        # delete templates after calling super, as deleting template could lead to deleting
        # products due to ondelete='cascade'
        self.pool.get('product.template').unlink(cr, uid, unlink_product_tmpl_ids, context=context)
        return res
    
#----------------------------------------------------------
# 计件工价
#----------------------------------------------------------
class piece_rate(osv.osv):
    _name = 'piece.rate'

    _columns = {
        'style_id': fields.many2one('style.no', u'款号', ondelete="cascade", required=True, select=True),
        'procedure_id': fields.many2one('work.procedure', u'工序', required=True, select=True),
        'procedure_uom': fields.related('procedure_id', 'uom_id', type='many2one', relation='product.uom', string=u'计量单位', readonly="1"),
        'rate': fields.float(u'工价', digits_compute=dp.get_precision('Product Price'), required=True),
    }
    _sql_constraints = [
        ('procedure_id', 'unique(style_id, procedure_id)', u'同款号工序不能重复'),
    ]
    _order = 'style_id, procedure_id'
    
    def onchange_procedure_id(self, cr, uid, ids, procedure_id):
        if procedure_id:
            uom_id = self.pool.get('work.procedure').browse(cr, uid, procedure_id).uom_id.id
            return {'value': {'procedure_uom': uom_id}}
        return {}
