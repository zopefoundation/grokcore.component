"""
  >>> grok.testing.grok(__name__)

  >>> cave = Cave()

  You can query the subscribers and sort them with the information
  provided by grok.order:

  >>> ordered_subscribers = grok.queryOrderedSubscriptions(cave, ICleaner)
  >>> ordered_subscribers
  [<grokcore.component.tests.subscriber.ordered_subscribers.MondayCleaner object at ...>,
   <grokcore.component.tests.subscriber.ordered_subscribers.WednesdayCleaner object at ...>,
   <grokcore.component.tests.subscriber.ordered_subscribers.SaturdayCleaner object at ...>]

  >>> _ = map(lambda s: s.work(), ordered_subscribers)
  Monday cleaning!
  Wednesday cleaning!
  Saturday cleaning!

  If you use the regular query method, they won't be sorted:

  >>> subscribers = grok.querySubscriptions(cave, ICleaner)
  >>> subscribers
  [<grokcore.component.tests.subscriber.ordered_subscribers.MondayCleaner object at ...>,
   <grokcore.component.tests.subscriber.ordered_subscribers.SaturdayCleaner object at ...>,
   <grokcore.component.tests.subscriber.ordered_subscribers.WednesdayCleaner object at ...>]

  >>> _ = map(lambda s: s.work(), subscribers)
  Monday cleaning!
  Saturday cleaning!
  Wednesday cleaning!

"""

import grokcore.component as grok
from zope import interface


class Cave(grok.Context):
    pass


class ICleaner(interface.Interface):

    def work():
        """Clean that cave.
        """

class MondayCleaner(grok.Subscription):
    grok.implements(ICleaner)
    grok.order(1)

    def work(self):
        print 'Monday cleaning!'


class WednesdayCleaner(grok.Subscription):
    grok.implements(ICleaner)
    grok.order(3)

    def work(self):
        print 'Wednesday cleaning!'


class SaturdayCleaner(grok.Subscription):
    grok.implements(ICleaner)
    grok.order(6)

    def work(self):
        print 'Saturday cleaning!'

