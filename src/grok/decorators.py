##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Grok
"""
import sys
import types
from zope.component._declaration import adapter as _adapter
from zope.interface.declarations import implementer as _implementer
from martian.error import GrokImportError

class adapter(_adapter):

    def __init__(self, *interfaces):
        # Override the z.c.adapter decorator to force sanity checking
        # and have better error reporting.
        if not interfaces:
            raise GrokImportError(
                "@grok.adapter requires at least one argument.")
        if type(interfaces[0]) is types.FunctionType:
            raise GrokImportError(
                "@grok.adapter requires at least one argument.")
        self.interfaces = interfaces

class implementer(_implementer):

    def __call__(self, ob):
        # XXX we do not have function grokkers (yet) so we put the annotation
        # on the module.
        frame = sys._getframe(1)
        implementers = frame.f_locals.get('__implementers__', None)
        if implementers is None:
            frame.f_locals['__implementers__'] = implementers = []
        implementers.append(ob)
        return _implementer.__call__(self, ob)
