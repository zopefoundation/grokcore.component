"""
You can register a named adapter by using grok.name:

  >>> grok.testing.grok(__name__)

  >>> cave = Cave()
  >>> home = IHome(cave)
  Traceback (most recent call last):
    ...
  TypeError: ('Could not adapt', <grokcore.component.tests.adapter.namedadapter.Cave object at 0x...>, <InterfaceClass grokcore.component.tests.adapter.namedadapter.IHome>)

  >>> from zope.component import getAdapter
  >>> home = getAdapter(cave, IHome, name='home')
  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True
"""  # noqa: E501 line too long

from zope import interface

import grokcore.component as grok


class Cave(grok.Context):
    pass


class IHome(interface.Interface):
    pass


@grok.implementer(IHome)
class Home(grok.Adapter):
    grok.name('home')
