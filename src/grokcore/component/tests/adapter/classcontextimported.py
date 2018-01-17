"""
Explicit class-level context for an imported model:

  >>> grok.testing.grok(__name__,
  ... 'grokcore.component.tests.adapter.adapter')

  >>> cave = Cave()
  >>> painting = IPainting(cave)

  >>> IPainting.providedBy(painting)
  True
  >>> isinstance(painting, Painting)
  True

"""
import grokcore.component as grok
from grokcore.component.tests.adapter.adapter import Cave
from zope import interface

class IPainting(interface.Interface):
    pass

@grok.implementer(IPainting)
class Painting(grok.Adapter):
    grok.context(Cave)
