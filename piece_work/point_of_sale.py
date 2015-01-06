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

class pos_order(osv.osv):
    _inherit = 'pos.order'

    def create_from_ui(self, cr, uid, orders, context=None):
        pw_line_pool = self.pool.get('piece.work.line')
        employee_pool = self.pool.get('hr.employee')
        product_pool = self.pool.get('product.product')
        rate_pool = self.pool.get('piece.rate')
        journal_pool = self.pool.get('account.journal')
        for o in orders:
            _logger.info("create_from_ui, order=%s", o['data'])
            partner_ids = employee_pool.search(cr, uid, [('partner_id','=',o['data']['partner_id'])])
            
            journal_id = False
            journal = False
            for stat in o['data']['statement_ids']:
                journal_id = stat[2]['journal_id']
            if journal_id:
                journal = journal_pool.browse(cr, uid, journal_id)
            for line in o['data']['lines']:
                product_id = line[2]['product_id']
                product = product_pool.browse(cr, uid, product_id)
                rate_ids = rate_pool.search(cr, uid, [('product_tmpl_id','=',product.product_tmpl_id.id)])
                rate = rate_pool.browse(cr, uid, rate_ids[0])
                pw_line_pool.create(cr, uid, {
                        'type': journal and journal.code == 'TCHK' and 'rework' or (journal and journal.code == 'TBNK' and 'scrap' or 'normal'),
                        'emp_id': partner_ids[0],
                        'style_id': rate.style_id.id,
                        'rate_id': rate_ids[0],
                        'unit_qty': line[2]['qty'],
                        'uom_id': rate.procedure_uom.id,
                    })
    
        return []
