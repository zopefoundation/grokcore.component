"""
Subclasses of grok.Adapter and grok.MultiAdapter must implement exactly one
interface:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grokcore.component.tests.adapter.implementsmany.Home'> is implementing
  more than one interface (use grok.provides to specify which one to use).
"""  # noqa: E501 line too long
from zope import interface

import grokcore.component as grok


class Cave(grok.Context):
    pass


class IHome(interface.Interface):
    pass


class IFireplace(interface.Interface):
    pass


@grok.implementer(IHome, IFireplace)
class Home(grok.Adapter):
    pass
