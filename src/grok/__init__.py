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
"""Grok
"""

from zope.interface import implements
from zope.component import adapts

from martian import ClassGrokker, InstanceGrokker, GlobalGrokker
from grok.components import Adapter, GlobalUtility, MultiAdapter, Context

from grok.directive import (context, name, title,
                            provides, baseclass, global_utility,
                            direct, order)
from grok.decorators import adapter, implementer
from martian.error import GrokError, GrokImportError

# BBB These two functions are meant for test fixtures and should be
# imported from grok.testing, not from grok.
from grok.testing import grok, grok_component

# Our __init__ provides the grok API directly so using 'import grok' is enough.
from grok.interfaces import IGrokAPI
from zope.interface import moduleProvides
moduleProvides(IGrokAPI)
__all__ = list(IGrokAPI)
