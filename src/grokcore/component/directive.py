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
import martian
import grokcore.component
from zope.interface.interfaces import IInterface
from martian.error import GrokImportError

class global_utility(martian.MultipleTimesDirective):
    scope = martian.MODULE

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
            name = grokcore.component.name.get(factory)
        self.name = name

class order(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    default = 0, 0

    _order = 0

    def factory(self, value=0):
        order._order += 1
        return value, order._order

class name(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    default = u''
    validate = martian.validateText

class context(martian.Directive):
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    validate = martian.validateInterfaceOrClass

class title(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateText

class direct(martian.MarkerDirective):
    scope = martian.CLASS

class provides(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateInterface
