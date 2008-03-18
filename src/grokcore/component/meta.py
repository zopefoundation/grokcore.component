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

from zope import component
import martian
from martian import util

import grokcore.component
from grokcore.component.util import check_adapts
from grokcore.component.util import check_module_component, determine_module_component
from grokcore.component.util import determine_class_component

def get_context(module_info, factory):
    return determine_class_component(module_info, factory,
                                     'context', 'grok.context')

def get_name_classname(factory):
    return get_name(factory, factory.__name__.lower())

def get_name(factory, default=''):
    return grokcore.component.util.class_annotation(factory, 'grok.name', default)

def get_provides(factory):
    provides = util.class_annotation(factory, 'grok.provides', None)
    if provides is None:
        util.check_implements_one(factory)
    return provides

class ContextGrokker(martian.GlobalGrokker):

    priority = 1001

    def grok(self, name, module, module_info, config, **kw):
        context = determine_module_component(module_info, 'grok.context',
                                             [grokcore.component.Context])
        module.__grok_context__ = context
        return True

class AdapterGrokker(martian.ClassGrokker):
    component_class = grokcore.component.Adapter

    def grok(self, name, factory, module_info, config, **kw):
        adapter_context = get_context(module_info, factory)
        provides = get_provides(factory)
        name = get_name(factory)
        
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
        name = get_name(factory)
        
        check_adapts(factory)
        for_ = component.adaptedBy(factory)

        config.action(
            discriminator=('adapter', for_, provides, name),
            callable=component.provideAdapter,
            args=(factory, None, provides, name),
            )
        return True

class GlobalUtilityGrokker(martian.ClassGrokker):
    component_class = grokcore.component.GlobalUtility

    # This needs to happen before the FilesystemPageTemplateGrokker grokker
    # happens, since it relies on the ITemplateFileFactories being grokked.
    priority = 1100

    def grok(self, name, factory, module_info, config, **kw):
        provides = get_provides(factory)
        name = get_name(factory)

        direct = util.class_annotation(factory, 'grok.direct', False)
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
        context = module_info.getAnnotation('grok.context', None)
        implementers = module_info.getAnnotation('implementers', [])
        for function in implementers:
            interfaces = getattr(function, '__component_adapts__', None)
            if interfaces is None:
                # There's no explicit interfaces defined, so we assume the
                # module context to be the thing adapted.
                check_module_component(module_info.getModule(), context,
                                       'context', 'grok.context')
                interfaces = (context, )

            config.action(
                discriminator=('adapter', interfaces, function.__implemented__),
                callable=component.provideAdapter,
                args=(function, interfaces, function.__implemented__),
                )
        return True


class GlobalUtilityDirectiveGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        infos = module_info.getAnnotation('grok.global_utility', [])

        for info in infos:
            if info.provides is None:
                util.check_implements_one(info.factory)
            if info.direct:
                obj = info.factory
            else:
                obj = info.factory()
            component.provideUtility(obj,
                                     provides=info.provides,
                                     name=info.name)
        return True
