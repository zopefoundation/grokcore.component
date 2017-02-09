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
"""Grok subscriptions functions.
"""
from zope.interface import providedBy
from grokcore.component import util

def queryOrderedMultiSubscriptions(components, interface):
    manager = util.getSiteManager()
    subscriptions = manager.adapters.subscriptions(
        map(providedBy, components), interface)
    results = []
    for subscription in util.sort_components(subscriptions):
        result = subscription(*components)
        if result is not None:
            results.append(result)
    return results

def queryOrderedSubscriptions(component, interface):
    return queryOrderedMultiSubscriptions((component, ), interface)

def queryMultiSubscriptions(components, interface):
    """Query for subscriptions on the `components` providing `interface`.

    :parameter components: tuple of components to lookup the subscription for.
    :parameter interface: interface that the subscriptions should provide.
    :return: a list of subscriptions.
    """
    manager = util.getSiteManager()
    subscriptions = manager.adapters.subscriptions(
        map(providedBy, components), interface)
    results = []
    for subscription in subscriptions:
        result = subscription(*components)
        if result is not None:
            results.append(result)
    return results

def querySubscriptions(component, interface):
    """Query for subscriptions on `component` providing `interface`.

    :parameter component: a component to lookup the subscriptions for.
    :parameter interface: interface that the subscriptions should provide.
    :return: a list of subscription.
    """
    return queryMultiSubscriptions((component,), interface)
