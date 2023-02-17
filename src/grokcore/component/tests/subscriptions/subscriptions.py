"""
  >>> grok.testing.grok(__name__)

  >>> cave = Cave('sweet home')

  >>> subscriptions = grok.querySubscriptions(cave, ICleaner)
  >>> subscriptions
  [<grokcore.component.tests.subscriptions.subscriptions.MondayCleaner object at ...>,
   <grokcore.component.tests.subscriptions.subscriptions.SaturdayCleaner object at ...>,
   <grokcore.component.tests.subscriptions.subscriptions.WednesdayCleaner object at ...>]

  >>> for s in subscriptions: s.work()
  Monday cleaning sweet home!
  Saturday cleaning sweet home!
  Wednesday cleaning sweet home!

  Subscription adapters are not registered as regular adapters:

  >>> from zope import component
  >>> component.queryAdapter(cave, ICleaner)

"""  # noqa: E501 line too long

from zope import interface

import grokcore.component as grok


class Cave(grok.Context):

    def __init__(self, name):
        self.name = name


class ICleaner(interface.Interface):

    def work():
        """Clean that cave."""


@grok.implementer(ICleaner)
class MondayCleaner(grok.Subscription):

    def work(self):
        print('Monday cleaning %s!' % self.context.name)


class WednesdayCleaner(grok.Subscription):
    grok.provides(ICleaner)

    def work(self):
        print('Wednesday cleaning %s!' % self.context.name)


@grok.implementer(ICleaner)
class SaturdayCleaner(grok.Subscription):

    def work(self):
        print('Saturday cleaning %s!' % self.context.name)
