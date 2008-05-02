##############################################################################
#
# Copyright (c) 2006-2007 Zope Corporation and Contributors.
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
import grokcore.component

from zope.interface.interfaces import IInterface

from martian.error import GrokImportError
from martian.directive import (OnceDirective,
                               MultipleTimesDirective,
                               SingleTextDirective,
                               MarkerDirective,
                               InterfaceDirective,
                               InterfaceOrClassDirective,
                               ModuleDirectiveContext,
                               OptionalValueDirective,
                               ClassDirectiveContext,
                               ClassOrModuleDirectiveContext)
from martian import util
from martian import ndir
from martian.ndir import baseclass

class global_utility(ndir.MultipleTimesDirective):
    scope = ndir.MODULE

    def factory(self, factory, provides=None, name=u'', direct=False):
        if provides is not None and not IInterface.providedBy(provides):
            raise GrokImportError(
                "You can only pass an interface to the "
                "provides argument of %s." % self.name)
        return GlobalUtilityInfo(factory, provides, name, direct)

class GlobalUtilityInfo(object):
    def __init__(self, factory, provides=None, name=u'', direct=None):
        self.factory = factory
        if direct is None:
            direct = grokcore.component.direct.get(factory)
        self.direct = direct

        if provides is None:
            provides = grokcore.component.provides.get(factory)
        self.provides = provides

        if name is u'':
            name = util.class_annotation(factory, 'grok.name', u'')
        self.name = name

class order(ndir.Directive):
    scope = ndir.CLASS
    store = ndir.ONCE

    _order = 0

    def factory(self, value=None):
        order._order += 1
        if value is not None:
            return value, order._order
        return super(order, self).factory(value)

    def default_value(self, component):
        return 0, order._order

class name(ndir.Directive):
    scope = ndir.CLASS
    store = ndir.ONCE
    validate = ndir.validateText

class context(ndir.Directive):
    scope = ndir.CLASS_OR_MODULE
    store = ndir.ONCE
    validate = ndir.validateInterfaceOrClass

class title(ndir.Directive):
    scope = ndir.CLASS
    store = ndir.ONCE
    validate = ndir.validateText

class direct(ndir.MarkerDirective):
    scope = ndir.CLASS

class provides(ndir.Directive):
    scope = ndir.CLASS
    store = ndir.ONCE
    validate = ndir.validateInterface
