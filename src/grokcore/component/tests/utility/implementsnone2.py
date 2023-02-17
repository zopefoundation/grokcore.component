"""
Subclasses of grok.GlobalUtility must implement exactly one interface:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grokcore.component.tests.utility.implementsnone2.Club'> must
  implement at least one interface (use grok.implements to specify).
"""  # noqa: E501 line too long
import grokcore.component as grok


class Club:
    pass


grok.global_utility(Club)
