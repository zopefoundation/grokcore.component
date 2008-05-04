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
import types
import martian
import grokcore.component
from zope.interface.interfaces import IInterface
from martian.error import GrokImportError
from grokcore.component.util import check_module_component

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

class name(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    default = u''
    validate = martian.validateText

class context(martian.Directive):
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    validate = martian.validateInterfaceOrClass

    @classmethod
    def get(cls, component, module=None):
        value = super(cls, context).get(component, module)
        if not isinstance(component, types.ModuleType):
            # 'component' must be a class then, so let's make sure
            # that the context is not ambiguous or None.
            check_module_component(component, value, 'context', cls)    
        return value

class title(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateText

class description(title):
    pass

class direct(martian.MarkerDirective):
    scope = martian.CLASS

class provides(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateInterface
