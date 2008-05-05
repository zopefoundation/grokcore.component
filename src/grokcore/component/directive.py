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
from grokcore.component.scan import check_module_component

class global_utility(martian.MultipleTimesDirective):
    scope = martian.MODULE

    def factory(self, factory, provides=None, name=u'', direct=False):
        if provides is not None and not IInterface.providedBy(provides):
            raise GrokImportError(
                "You can only pass an interface to the "
                "provides argument of %s." % self.name)

        if provides is None:
            provides = grokcore.component.provides.bind().get(factory)
        if direct is None:
            direct = grokcore.component.direct.bind().get(factory)
        if not name:
            name = grokcore.component.name.bind().get(factory)
        return (factory, provides, name, direct)

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
    def check_value(cls, value, component, module=None, **data):
        if not isinstance(component, types.ModuleType):
            # 'component' must be a class then, so let's make sure
            # that the context is not ambiguous or None.
            check_module_component(component, value, 'context', cls)    

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
