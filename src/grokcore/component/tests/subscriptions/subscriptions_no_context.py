"""
  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: No module-level context for
  <class 'grokcore.component.tests.subscriptions.subscriptions_no_context.CaveProcessor'>,
  please use the 'context' directive.

"""  # noqa: E501 line too long

from zope import interface

import grokcore.component as grok


class ITask(interface.Interface):

    def finish():
        pass


class CaveProcessor(grok.Subscription):
    grok.provides(ITask)
