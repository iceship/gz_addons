# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    Jeroen Vet, eXcec Business Consulting Ltd.  vet@excecbc.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.addons.product.product import product_template

def write(self, cr, uid, ids, vals, context=None):
    ''' Store the standard price change in order to be able to retrieve the cost of a product template for a given date'''
    if isinstance(ids, (int, long)):
        ids = [ids]
    if 'uom_po_id' in vals:
        new_uom = self.pool.get('product.uom').browse(cr, uid, vals['uom_po_id'], context=context)
        for product in self.browse(cr, uid, ids, context=context):
            old_uom = product.uom_po_id
            if old_uom.category_id.id != new_uom.category_id.id:
                #raise osv.except_osv(_('Unit of Measure categories Mismatch!'), _("New Unit of Measure '%s' must belong to same Unit of Measure category '%s' as of old Unit of Measure '%s'. If you need to change the unit of measure, you may deactivate this product from the 'Procurements' tab and create a new one.") % (new_uom.name, old_uom.category_id.name, old_uom.name,))
                if self.pool.get('stock.move').search(cr, uid, [('product_id', 'in', [x.id for x in product.product_variant_ids])], context=context):
                    raise osv.except_osv(_('Unit of Measure categories Mismatch!'), _("New Unit of Measure '%s' must belong to same Unit of Measure category '%s' as of old Unit of Measure '%s'. If you need to change the unit of measure, you may deactivate this product from the 'Procurements' tab and create a new one.") % (new_uom.name, old_uom.category_id.name, old_uom.name,))   
    if 'standard_price' in vals:
        for prod_template_id in ids:
            self._set_standard_price(cr, uid, prod_template_id, vals['standard_price'], context=context)
    res = super(product_template, self).write(cr, uid, ids, vals, context=context)
    if 'attribute_line_ids' in vals or vals.get('active'):
        self.create_variant_ids(cr, uid, ids, context=context)
    if 'active' in vals and not vals.get('active'):
        ctx = context and context.copy() or {}
        ctx.update(active_test=False)
        product_ids = []
        for product in self.browse(cr, uid, ids, context=ctx):
            product_ids = map(int,product.product_variant_ids)
        self.pool.get("product.product").write(cr, uid, product_ids, {'active': vals.get('active')}, context=ctx)
    return res

product_template.write = write
