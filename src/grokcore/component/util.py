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
"""Grok utility functions.
"""

import grokcore.component
from zope import component, interface

from martian.error import GrokError
from martian.util import methods_from_class, scan_for_classes

def check_adapts(class_):
    if component.adaptedBy(class_) is None:
        raise GrokError("%r must specify which contexts it adapts "
                        "(use grok.adapts to specify)."
                        % class_, class_)

def _sort_key(component):
    explicit_order, implicit_order = grokcore.component.order.get(component)
    return (explicit_order,
            component.__module__,
            implicit_order,
            component.__class__.__name__)

def sort_components(components):
    # if components have a grok.order directive, sort by that
    return sorted(components, key=_sort_key)

AMBIGUOUS_COMPONENT = object()
def check_module_component(factory, component, component_name, directive):
    """Raise error if module-level component cannot be determined.

    If the module-level component is None, it's never been specified;
    raise error telling developer to specify.

    if the module-level component is AMBIGUOUS_COMPONENT, raise
    an error telling developer to specify which one to use.
    """
    if component is None:
        raise GrokError("No module-level %s for %r, please use the '%s' "
                        "directive."
                        % (component_name, factory, directive.__name__),
                        factory)
    elif component is AMBIGUOUS_COMPONENT:
        raise GrokError("Multiple possible %ss for %r, please use the '%s' "
                        "directive."
                        % (component_name, factory, directive.__name__),
                        factory)

def determine_module_component(module_info, directive, classes):
    """Determine module-level component.

    The module-level component can be set explicitly using the
    annotation (such as grok.context).

    If there is no annotation, the module-level component is determined
    by scanning for subclasses of any in the list of classes.

    If there is no module-level component, the module-level component is
    None.

    If there is one module-level component, it is returned.

    If there are more than one module-level component, AMBIGUOUS_COMPONENT
    is returned.
    """
    module = module_info.getModule()
    components = scan_for_classes(module, classes)
    if len(components) == 0:
        component = None
    elif len(components) == 1:
        component = components[0]
    else:
        component= AMBIGUOUS_COMPONENT

    module_component = directive.get(module)
    if module_component is not None:
        component = module_component
    return component


def check_provides_one(obj):
    provides = list(interface.providedBy(obj))
    if len(provides) < 1:
        raise GrokError("%r must provide at least one interface "
                        "(use zope.interface.classProvides to specify)."
                        % obj, obj)
    if len(provides) > 1:
        raise GrokError("%r provides more than one interface "
                        "(use grok.provides to specify which one to use)."
                        % obj, obj)
