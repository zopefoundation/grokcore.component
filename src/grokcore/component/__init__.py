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
# flake8: noqa F401

from martian import ClassGrokker
from martian import GlobalGrokker
from martian import InstanceGrokker
from martian import baseclass
from martian import ignore
from martian.error import GrokError
from martian.error import GrokImportError
from zope.component import adapts

# Import this module so that it's available as soon as you import the
# 'grokcore.component' package.  Useful for tests and interpreter examples.
import grokcore.component.testing
from grokcore.component.components import Adapter
from grokcore.component.components import Context
from grokcore.component.components import GlobalUtility
from grokcore.component.components import MultiAdapter
from grokcore.component.components import MultiSubscription
from grokcore.component.components import Subscription
from grokcore.component.decorators import adapter
from grokcore.component.decorators import implementer
from grokcore.component.decorators import provider
from grokcore.component.decorators import subscribe
from grokcore.component.directive import context
from grokcore.component.directive import description
from grokcore.component.directive import direct
from grokcore.component.directive import global_adapter
from grokcore.component.directive import global_utility
from grokcore.component.directive import implements
from grokcore.component.directive import name
from grokcore.component.directive import order
from grokcore.component.directive import path
from grokcore.component.directive import provides
from grokcore.component.directive import title
from grokcore.component.interfaces import IGrokcoreComponentAPI
from grokcore.component.subscription import queryMultiSubscriptions
from grokcore.component.subscription import queryOrderedMultiSubscriptions
from grokcore.component.subscription import queryOrderedSubscriptions
from grokcore.component.subscription import querySubscriptions
from grokcore.component.util import getSiteManager
from grokcore.component.util import provideAdapter
from grokcore.component.util import provideHandler
from grokcore.component.util import provideInterface
from grokcore.component.util import provideSubscriptionAdapter
from grokcore.component.util import provideUtility
from grokcore.component.util import sort_components


adapts.__doc__ = "Declares the types of objects that a multi-adapter adapts."
# Only export public API
__all__ = list(IGrokcoreComponentAPI)
