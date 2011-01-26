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
"""Grok utility functions.
"""
from grokcore.component import directive
from zope import component

def _sort_key(component):
    # If components have a grok.order directive, sort by that.
    explicit_order, implicit_order = directive.order.bind().get(component)
    return (explicit_order,
            component.__module__,
            implicit_order,
            component.__class__.__name__)


def sort_components(components):
    """Sort a list of components using the information provided by
    `grok.order`.
    """
    return sorted(components, key=_sort_key)


def queryOrderedSubscribers(components, interface):
    return sort_components(component.subscribers(components, interface))


def querySubscribers(components, interface):
    """Query a list of subscribers on `component` which implements
    `interface`.

    :parameter components: list of components to look the subscribers for.
    :parameter interface: interface that the subscribers should provides.
    :return: a list of subscribers.
    """
    return component.subscribers(components, interface)
