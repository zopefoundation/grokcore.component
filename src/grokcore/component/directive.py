##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
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
"""Grok directives.
"""
import martian
import martian.util
from martian.error import GrokError, GrokImportError
from martian.util import scan_for_classes
from zope import interface
from zope.interface.interfaces import IInterface
from grokcore.component.interfaces import IContext

class global_utility(martian.MultipleTimesDirective):
    scope = martian.MODULE

    def factory(self, factory, provides=None, name=u'', direct=False):
        if provides is not None and not IInterface.providedBy(provides):
            raise GrokImportError(
                "You can only pass an interface to the "
                "provides argument of %s." % self.name)
        return (factory, provides, name, direct)

class global_adapter(martian.MultipleTimesDirective):
    scope = martian.MODULE

    def factory(self, factory, adapts=None, provides=None, name=u''):
        if provides is not None and not IInterface.providedBy(provides):
            raise GrokImportError(
                "You can only pass an interface to the "
                "provides argument of %s." % self.name)
        if not isinstance(adapts, (list, tuple,)):
            adapts = (adapts,)
        elif isinstance(adapts, list):
            adapts = tuple(adapts)

        return (factory, adapts, provides, name)

class name(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateText
    default = u''

class context(martian.Directive):
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    validate = martian.validateInterfaceOrClass

    @classmethod
    def get_default(cls, component, module=None, **data):
        components = list(scan_for_classes(module, IContext))
        if len(components) == 0:
            raise GrokError(
                "No module-level context for %r, please use the 'context' "
                "directive." % (component), component)
        elif len(components) == 1:
            component = components[0]
        else:
            raise GrokError(
                "Multiple possible contexts for %r, please use the 'context' "
                "directive."
                % (component), component)
        return component

class title(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateText

class description(title):
    pass

class direct(martian.MarkerDirective):
    scope = martian.CLASS

class order(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    default = 0, 0

    _order = 0

    def factory(self, value=0):
        order._order += 1
        return value, order._order

class path(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateText

class provides(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateInterface

    @classmethod
    def get_default(cls, component, module, **data):
        martian.util.check_implements_one(component)
        return list(interface.implementedBy(component))[0]
