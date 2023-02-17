"""
Multiple models lead to ambiguity:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Multiple possible contexts for
  <class 'grokcore.component.tests.adapter.multiple.Home'>, please use the
  'context' directive.

"""
from zope import interface

import grokcore.component as grok


class Cave(grok.Context):
    pass


class Club(grok.Context):
    pass


class IHome(interface.Interface):
    pass


@grok.implementer(IHome)
class Home(grok.Adapter):
    pass
