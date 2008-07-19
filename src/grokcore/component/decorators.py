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
import zope.component
import zope.interface
from martian.util import frame_is_module
from martian.error import GrokImportError

class subscribe:

    def __init__(self, *args):
        self.subscribed = args

    def __call__(self, function):
        frame = sys._getframe(1)
        if not frame_is_module(frame):
            raise GrokImportError("@grok.subscribe can only be used on module "
                                  "level.")

        if not self.subscribed:
            raise GrokImportError("@grok.subscribe requires at least one "
                                  "argument.")

        subscribers = frame.f_locals.get('__grok_subscribers__', None)
        if subscribers is None:
            frame.f_locals['__grok_subscribers__'] = subscribers = []
        subscribers.append((function, self.subscribed))
        return function

class adapter(zope.component.adapter):

    # Override the z.c.adapter decorator to force sanity checking and
    # have better error reporting.

    def __init__(self, *interfaces):
        if not interfaces:
            raise GrokImportError(
                "@grok.adapter requires at least one argument.")
        if type(interfaces[0]) is types.FunctionType:
            raise GrokImportError(
                "@grok.adapter requires at least one argument.")

        zope.component.adapter.__init__(self, *interfaces)

class implementer(zope.interface.implementer):

    def __call__(self, ob):
        # XXX we do not have function grokkers (yet) so we put the annotation
        # on the module.
        frame = sys._getframe(1)
        adapters = frame.f_locals.get('__grok_adapters__', None)
        if adapters is None:
            frame.f_locals['__grok_adapters__'] = adapters = []
        adapters.append(ob)
        return zope.interface.implementer.__call__(self, ob)
