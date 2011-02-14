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
"""Grok
"""

from zope.component import adapts
adapts.__doc__ = "Declares the types of objects that a multi-adapter adapts."

from zope.interface import implements, implementsOnly, classProvides

from martian import baseclass
from martian.error import GrokError, GrokImportError
from martian import ClassGrokker, InstanceGrokker, GlobalGrokker

from grokcore.component.components import (
    Adapter, GlobalUtility, MultiAdapter, Context, Subscription,
    MultiSubscription)

from grokcore.component.directive import (
    context, description, direct, name, order, path, provides, title,
    global_utility, global_adapter, order)

from grokcore.component.decorators import (
    subscribe, adapter, implementer, provider)

from grokcore.component.subscription import (
    querySubscriptions, queryMultiSubscriptions,
    queryOrderedSubscriptions, queryOrderedMultiSubscriptions)

# Import this module so that it's available as soon as you import the
# 'grokcore.component' package.  Useful for tests and interpreter examples.
import grokcore.component.testing

# Only export public API
from grokcore.component.interfaces import IGrokcoreComponentAPI
__all__ = list(IGrokcoreComponentAPI)
