"""
Subclasses of grok.Adapter and grok.MultiAdapter must implement exactly one
interface:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grokcore.component.tests.adapter.implementsnone.Home'> must
  implement at least one interface (use grok.implements to specify).
"""  # noqa: E501 line too long
import grokcore.component as grok


class Cave(grok.Context):
    pass


class Home(grok.Adapter):
    pass
