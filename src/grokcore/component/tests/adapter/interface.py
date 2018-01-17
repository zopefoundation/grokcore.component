"""
You can also specify interfaces instead of classes with
`grok.context` (class-level):

  >>> grok.testing.grok(__name__)

  >>> cave = Cave()
  >>> home = IHome(cave)

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True

  >>> hole = Hole()
  >>> home = IHome(hole)

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True

"""
import grokcore.component as grok
from zope import interface

class ICave(interface.Interface):
    pass

@grok.implementer(ICave)
class Cave(grok.Context):
    pass

@grok.implementer(ICave)
class Hole(grok.Context):
    pass

class IHome(interface.Interface):
    pass

@grok.implementer(IHome)
class Home(grok.Adapter):
    grok.context(ICave)
