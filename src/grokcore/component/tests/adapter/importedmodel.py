"""
Imported model and adapter won't be grokked:

  >>> import grokcore.component as grok
  >>> grok.testing.grok(__name__)
  >>> from grokcore.component.tests.adapter.adapter import IHome
  >>> cave = Cave()
  >>> home = IHome(cave)
  Traceback (most recent call last):
    ...
  TypeError: ('Could not adapt', <grokcore.component.tests.adapter.adapter.Cave object at ...>, <InterfaceClass grokcore.component.tests.adapter.adapter.IHome>)

"""  # noqa: E501 line too long
from grokcore.component.tests.adapter.adapter import Cave  # noqa: F401
from grokcore.component.tests.adapter.adapter import Home  # noqa: F401
