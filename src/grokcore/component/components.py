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
"""Grok components"""

from zope.interface import implements

from grokcore.component.interfaces import IContext

class Adapter(object):
    """Base class to define an adapter.

    Adapters are automatically registered when a module is "grokked".

    .. attribute:: context

       The adapted object.
    
    """
    def __init__(self, context):
        self.context = context

class GlobalUtility(object):
    pass

class MultiAdapter(object):
    """Base class to define a Multi Adapter.
    """
    pass

class Context(object):
    implements(IContext)
