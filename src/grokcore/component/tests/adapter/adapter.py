"""
  >>> grok.testing.grok(__name__)

  >>> cave = Cave()
  >>> home = IHome(cave)

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True

  >>> fireplace = IFireplace(cave)
  >>> IFireplace.providedBy(fireplace)
  True
  >>> isinstance(fireplace, Fireplace)
  True
"""

from zope import interface

import grokcore.component as grok


class Cave(grok.Context):
    pass


class IHome(interface.Interface):
    pass


@grok.implementer(IHome)
class Home(grok.Adapter):
    pass


class IFireplace(interface.Interface):
    pass


@grok.implementer(IFireplace, IHome)
class Fireplace(grok.Adapter):
    grok.provides(IFireplace)


SweetHome = Home
grok.ignore('SweetHome')
