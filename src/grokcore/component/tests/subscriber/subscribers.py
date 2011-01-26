"""
  >>> grok.testing.grok(__name__)

  >>> cave = Cave('sweet home')

  >>> subscribers = grok.querySubscribers((cave,), ICleaner)
  >>> subscribers
  [<grokcore.component.tests.subscriber.subscribers.MondayCleaner object at ...>,
   <grokcore.component.tests.subscriber.subscribers.SaturdayCleaner object at ...>,
   <grokcore.component.tests.subscriber.subscribers.WednesdayCleaner object at ...>]

  >>> _ = map(lambda s: s.work(), subscribers)
  Monday cleaning sweet home!
  Saturday cleaning sweet home!
  Wednesday cleaning sweet home!

"""

import grokcore.component as grok
from zope import interface


class Cave(grok.Context):

    def __init__(self, name):
        self.name = name


class ICleaner(interface.Interface):

    def work():
        """Clean that cave.
        """

class MondayCleaner(grok.Subscriber):
    grok.implements(ICleaner)

    def work(self):
        print 'Monday cleaning %s!' % self.context.name


class WednesdayCleaner(grok.Subscriber):
    grok.provides(ICleaner)

    def work(self):
        print 'Wednesday cleaning %s!' % self.context.name


class SaturdayCleaner(grok.Subscriber):
    grok.implements(ICleaner)

    def work(self):
        print 'Saturday cleaning %s!' % self.context.name

