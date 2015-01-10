# -*- coding: utf-8 -*-

__all__ = ['WechatBasic', 'WechatExt']

try:
    from .basic import WechatBasic
    from .ext import WechatExt
except ImportError:
    pass