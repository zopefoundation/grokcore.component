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

import martian
import martian.util
import grokcore.component
import zope.component.interface

from zope import component, interface
from martian.error import GrokError
from grokcore.component.scan import check_module_component
from grokcore.component.scan import determine_module_component
from grokcore.component.interfaces import IContext


def default_provides(factory, module=None, **data):
    martian.util.check_implements_one(factory)
    return list(interface.implementedBy(factory))[0]

def default_global_utility_provides(factory, module, direct, **data):
    if direct:
        martian.util.check_provides_one(factory)
        return list(interface.providedBy(factory))[0]
    return default_provides(factory)


class ContextGrokker(martian.GlobalGrokker):

    martian.priority(1001)

    def grok(self, name, module, module_info, config, **kw):
        context = determine_module_component(module_info,
                                             grokcore.component.context,
                                             IContext)
        grokcore.component.context.set(module, context)
        return True


class AdapterGrokker(martian.ClassGrokker):
    martian.component(grokcore.component.Adapter)

    martian.directive(grokcore.component.context)
    martian.directive(grokcore.component.provides,
                      get_default=default_provides)
    martian.directive(grokcore.component.name)
    
    def execute(self, factory, config, context, provides, name, **kw):
        config.action(
            discriminator=('adapter', context, provides, name),
            callable=component.provideAdapter,
            args=(factory, (context,), provides, name),
            )
        return True


class MultiAdapterGrokker(martian.ClassGrokker):
    martian.component(grokcore.component.MultiAdapter)

    martian.directive(grokcore.component.provides,
                      get_default=default_provides)
    martian.directive(grokcore.component.name)

    def execute(self, factory, config, provides, name, **kw):
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


class GlobalUtilityGrokker(martian.ClassGrokker):
    martian.component(grokcore.component.GlobalUtility)

    # This needs to happen before the FilesystemPageTemplateGrokker grokker
    # happens, since it relies on the ITemplateFileFactories being grokked.
    martian.priority(1100)

    martian.directive(grokcore.component.direct)
    martian.directive(grokcore.component.provides,
                      get_default=default_global_utility_provides)
    martian.directive(grokcore.component.name)

    def execute(self, factory, config, direct, provides, name, **kw):
        if not direct:
            factory = factory()

        config.action(
            discriminator=('utility', provides, name),
            callable=component.provideUtility,
            args=(factory, provides, name),
            )
        return True

class AdapterDecoratorGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        context = grokcore.component.context.bind().get(module=module)
        adapters = module_info.getAnnotation('grok.adapters', [])
        for function in adapters:
            interfaces = getattr(function, '__component_adapts__', None)
            if interfaces is None:
                # There's no explicit interfaces defined, so we assume the
                # module context to be the thing adapted.
                check_module_component(function, context, 'context',
                                       grokcore.component.context)
                interfaces = (context, )
            name = getattr(function, '__component_name__', u"")
            config.action(
                discriminator=('adapter', interfaces, function.__implemented__, name),
                callable=component.provideAdapter,
                args=(function, interfaces, function.__implemented__, name),
                )
        return True


class GlobalUtilityDirectiveGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        infos = grokcore.component.global_utility.bind().get(module=module)

        for factory, provides, name, direct in infos:
            if direct:
                obj = factory
                if provides is None:
                    martian.util.check_provides_one(obj)
                    provides = list(interface.providedBy(obj))[0]
            else:
                obj = factory()
                if provides is None:
                    provides = default_provides(factory)

            config.action(
                discriminator=('utility', provides, name),
                callable=component.provideUtility,
                args=(obj, provides, name),
                )

        return True

class GlobalAdapterDirectiveGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        infos = grokcore.component.global_adapter.bind().get(module=module)

        for factory, adapts, provides, name in infos:
            config.action(
                discriminator=('adapter', adapts, provides, name),
                callable=component.provideAdapter,
                args=(factory, adapts, provides, name),
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
