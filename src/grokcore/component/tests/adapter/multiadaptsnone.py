"""
Subclasses of grok.MultiAdapter must declare what they adapt, using grok.adapts:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grokcore.component.tests.adapter.multiadaptsnone.Home'>
  must specify which contexts it adapts (use the 'adapts' directive to specify).
"""  # noqa: E501 line too long
from zope import interface

import grokcore.component as grok


class IHome(interface.Interface):
    pass


@grok.implementer(IHome)
class Home(grok.MultiAdapter):
    pass
