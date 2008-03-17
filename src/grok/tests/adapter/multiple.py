"""
Multiple models lead to ambiguity:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Multiple possible contexts for
  <class 'grok.tests.adapter.multiple.Home'>, please use grok.context.

"""
import grok
from zope import interface

class Cave(grok.Context):
    pass

class Club(grok.Context):
    pass

class IHome(interface.Interface):
    pass

class Home(grok.Adapter):
    grok.implements(IHome)
