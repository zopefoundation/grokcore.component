"""
Explicit class-level context in case of multiple models:

  >>> grok.testing.grok(__name__)

  >>> cave = Cave()
  >>> home = IHome(cave)

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True

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
    grok.context(Cave)
