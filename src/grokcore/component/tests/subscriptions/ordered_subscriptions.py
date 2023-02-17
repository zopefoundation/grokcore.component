"""
  >>> grok.testing.grok(__name__)

  >>> cave = Cave()

  You can query the subscriptions and sort them with the information
  provided by grok.order:

  >>> ordered_subscriptions = grok.queryOrderedSubscriptions(cave, ICleaner)
  >>> ordered_subscriptions
  [<grokcore.component.tests.subscriptions.ordered_subscriptions.MondayCleaner object at ...>,
   <grokcore.component.tests.subscriptions.ordered_subscriptions.WednesdayCleaner object at ...>,
   <grokcore.component.tests.subscriptions.ordered_subscriptions.SaturdayCleaner object at ...>]

  >>> for s in ordered_subscriptions: s.work()
  Monday cleaning!
  Wednesday cleaning!
  Saturday cleaning!

  If you use the regular query method, they won't be sorted:

  >>> subscriptions = grok.querySubscriptions(cave, ICleaner)
  >>> subscriptions
  [<grokcore.component.tests.subscriptions.ordered_subscriptions.MondayCleaner object at ...>,
   <grokcore.component.tests.subscriptions.ordered_subscriptions.SaturdayCleaner object at ...>,
   <grokcore.component.tests.subscriptions.ordered_subscriptions.WednesdayCleaner object at ...>]

  >>> for s in subscriptions: s.work()
  Monday cleaning!
  Saturday cleaning!
  Wednesday cleaning!

"""   # noqa: E501 line too long

from zope import interface

import grokcore.component as grok


class Cave(grok.Context):
    pass


class ICleaner(interface.Interface):

    def work():
        """Clean that cave.
        """


@grok.implementer(ICleaner)
class MondayCleaner(grok.Subscription):
    grok.order(1)

    def work(self):
        print('Monday cleaning!')


@grok.implementer(ICleaner)
class WednesdayCleaner(grok.Subscription):
    grok.order(3)

    def work(self):
        print('Wednesday cleaning!')


@grok.implementer(ICleaner)
class SaturdayCleaner(grok.Subscription):
    grok.order(6)

    def work(self):
        print('Saturday cleaning!')
