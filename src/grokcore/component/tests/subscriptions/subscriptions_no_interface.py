"""
  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grokcore.component.tests.subscriptions.subscriptions_no_interface.CaveProcessor'>
  must implement at least one interface (use grok.implements to specify).

"""  # noqa: E501 line too long

import grokcore.component as grok


class Cave(grok.Context):
    pass


class CaveProcessor(grok.Subscription):
    pass
