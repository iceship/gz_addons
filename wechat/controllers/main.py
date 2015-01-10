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
import time
import logging
from openerp import http, SUPERUSER_ID
from openerp.http import request
from wechat_sdk import WechatBasic

_logger = logging.getLogger(__name__)

class WechatController(http.Controller):

    @http.route('/wechat', type='http', auth='public', methods=['GET'])
    def check_signature(self, **post):
        _logger.info('post are %s', post)
        wechat = WechatBasic(token="gongzi")
        if wechat.check_signature(signature=post.get('signature'), timestamp=post.get('timestamp'), nonce=post.get('nonce')):
            return post.get('echostr')
        return 'Error'
