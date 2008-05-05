#############################################################################
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
"""Grokkers for the various components."""

import martian.util
import grokcore.component
import zope.component.interface

from zope import component, interface
from martian.error import GrokError
from grokcore.component.scan import check_module_component
from grokcore.component.scan import determine_module_component
from grokcore.component.interfaces import IContext
from grokcore.component.interfaces import IContext

def get_provides(factory):
    provides = grokcore.component.provides.get(factory)

    if provides is None:
        martian.util.check_implements_one(factory)
        provides = list(interface.implementedBy(factory))[0]
    return provides


class ContextGrokker(martian.GlobalGrokker):

    priority = 1001

    def grok(self, name, module, module_info, config, **kw):
        context = determine_module_component(module_info,
                                             grokcore.component.context,
                                             IContext)
        grokcore.component.context.set(module, context)
        return True


class AdapterGrokker(martian.ClassGrokker):
    component_class = grokcore.component.Adapter

    def grok(self, name, factory, module_info, config, **kw):
        adapter_context = grokcore.component.context.get(factory, module_info.getModule())
        provides = get_provides(factory)
        name = grokcore.component.name.get(factory)

        config.action(
            discriminator=('adapter', adapter_context, provides, name),
            callable=component.provideAdapter,
            args=(factory, (adapter_context,), provides, name),
            )
        return True


class MultiAdapterGrokker(martian.ClassGrokker):
    component_class = grokcore.component.MultiAdapter

    def grok(self, name, factory, module_info, config, **kw):
        provides = get_provides(factory)
        name = grokcore.component.name.get(factory)

        if component.adaptedBy(factory) is None:
            raise GrokError("%r must specify which contexts it adapts "
                            "(use the 'adapts' directive to specify)."
                            % factory, factory)
        for_ = component.adaptedBy(factory)

        config.action(
            discriminator=('adapter', for_, provides, name),
            callable=component.provideAdapter,
            args=(factory, None, provides, name),
            )
        return True


def default_global_utility_provides(factory, module, direct, **data):
    if direct:
        if provides is None:
            martian.util.check_provides_one(factory)
            provides = list(interface.providedBy(factory))[0]
    else:
        if provides is None:
            provides = get_provides(factory)
    return provides


class GlobalUtilityGrokker(martian.ClassGrokker):
    component_class = grokcore.component.GlobalUtility

    # This needs to happen before the FilesystemPageTemplateGrokker grokker
    # happens, since it relies on the ITemplateFileFactories being grokked.
    priority = 1100

    directives = [
        grokcore.component.direct.bind(),
        grokcore.component.provides.bind(
            get_default=default_global_utility_provides),
        grokcore.component.provides.bind(default=IFoo),
        grokcore.component.name.bind(),
        ]


    def register(self, factory, config, direct, provides, name):
        if not direct:
            factory = factory()

        config.action(
            discriminator=('utility', provides, name),
            callable=component.provideUtility,
            args=(obj, provides, name),
            )
        return True


    def grok(self, name, factory, module_info, config, **kw):
        module = module_info.getModule()

        # Populate the data dict with information from the directives:
        data = {}
        for bound_directive in self.directives:
            data[dirname] = bound_directive.get(factory, module, **data)
        return self.register(factory, config, **data)


class Directive(...):

    @classmethod
    def bind(cls, default=None, get_default=None, name=None):
        return BoundDirective(cls, default, get_default, name)


class BoundDirective(object):

    def __init__(self, directive, default=None, get_default=None, name=None):
        self.directive = directive
        self.default = default
        if name is None:
            name = directive.__name__
        self.name = name
        if get_default is not None:
            self.get_default = get_default

    def get_default(self, component, module, **data):
        if self.default is not None:
            return self.default
        return self.directive.default

    def get(self, component, module, **data):
        value = self.directive.get(component, module, default=_DEFAULT)
        if value is _DEFAULT:
            value = self.get_default(component, module, **data)
        return value


class AdapterDecoratorGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        context = grokcore.component.context.get(module)
        implementers = module_info.getAnnotation('implementers', [])
        for function in implementers:
            interfaces = getattr(function, '__component_adapts__', None)
            if interfaces is None:
                # There's no explicit interfaces defined, so we assume the
                # module context to be the thing adapted.
                check_module_component(function, context, 'context',
                                       grokcore.component.context)
                interfaces = (context, )

            config.action(
                discriminator=('adapter', interfaces, function.__implemented__),
                callable=component.provideAdapter,
                args=(function, interfaces, function.__implemented__),
                )
        return True


class GlobalUtilityDirectiveGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        infos = grokcore.component.global_utility.get(module)

        for info in infos:
            provides = info.provides

            if info.direct:
                obj = info.factory
                if provides is None:
                    martian.util.check_provides_one(obj)
                    provides = list(interface.providedBy(obj))[0]
            else:
                obj = info.factory()
                if provides is None:
                    provides = get_provides(info.factory)

            config.action(
                discriminator=('utility', provides, info.name),
                callable=component.provideUtility,
                args=(obj, provides, info.name),
                )

        return True


class SubscriberGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        subscribers = module_info.getAnnotation('grok.subscribers', [])

        for factory, subscribed in subscribers:
            config.action(
                discriminator=None,
                callable=component.provideHandler,
                args=(factory, subscribed),
                )

            for iface in subscribed:
                config.action(
                    discriminator=None,
                    callable=zope.component.interface.provideInterface,
                    args=('', iface)
                    )
        return True
