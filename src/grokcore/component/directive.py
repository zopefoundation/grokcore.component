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

class GlobalUtilityDirective(MultipleTimesDirective):
    def check_arguments(self, factory, provides=None, name=u'',
                        direct=False):
        if provides is not None and not IInterface.providedBy(provides):
            raise GrokImportError("You can only pass an interface to the "
                                  "provides argument of %s." % self.name)

    def value_factory(self, *args, **kw):
        return GlobalUtilityInfo(*args, **kw)


class GlobalUtilityInfo(object):
    def __init__(self, factory, provides=None, name=u'', direct=None):
        self.factory = factory
        if direct is None:
            direct = util.class_annotation(factory, 'grok.direct', False)
        self.direct = direct

        if provides is None:
            provides = util.class_annotation(factory, 'grok.provides', None)
        self.provides = provides

        if name is u'':
            name = util.class_annotation(factory, 'grok.name', u'')
        self.name = name


class MultiValueOnceDirective(OnceDirective):

    def check_arguments(self, *values):
        pass

    def value_factory(self, *args):
        return args

class OrderDirective(OptionalValueDirective, OnceDirective):

    order = 0

    def value_factory(self, value=None):
        OrderDirective.order += 1
        if value is not None:
            return value, OrderDirective.order
        return super(OrderDirective, self).value_factory(value)

    def default_value(self):
        return 0, OrderDirective.order

# Define grok directives
name = SingleTextDirective('grok.name', ClassDirectiveContext())
context = InterfaceOrClassDirective('grok.context',
                                    ClassOrModuleDirectiveContext())
provides = InterfaceDirective('grok.provides', ClassDirectiveContext())
baseclass = MarkerDirective('grok.baseclass', ClassDirectiveContext())
global_utility = GlobalUtilityDirective('grok.global_utility',
                                        ModuleDirectiveContext())
title = SingleTextDirective('grok.title', ClassDirectiveContext())
order = OrderDirective('grok.order', ClassDirectiveContext())
direct = MarkerDirective('grok.direct', ClassDirectiveContext())
