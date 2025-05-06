"""
  >>> grok.testing.grok(__name__)

  >>> cave = Cave('Tilburg cave')
  >>> martijn = Mammoth('Martijn')

  You can query a subscriptions using multiple components. You will get
  all subscriptions registered for office and cave (since office is a
  base class of cave):

  >>> subscriptions = grok.queryMultiSubscriptions((cave, martijn), IActivity)
  >>> subscriptions
  [<grokcore.component.tests.subscriptions.multisubscriptions.Sleep object at ...>,
   <grokcore.component.tests.subscriptions.multisubscriptions.Food object at ...>,
   <grokcore.component.tests.subscriptions.multisubscriptions.WritingCode object at ...>]

  >>> for s in subscriptions: s.do()
  Martijn is sleeping at Tilburg cave.
  Martijn is feeding himself at Tilburg cave.
  Martijn is writing code at Tilburg cave!


  Now, Martijn goes to the office. You will only get subscriptions
  registered for office:

  >>> office = Office('Grok corp(r)(tm) headquarters')
  >>> office_subscriptions = grok.queryMultiSubscriptions(
  ...     (office, martijn), IActivity)
  >>> office_subscriptions
  [<grokcore.component.tests.subscriptions.multisubscriptions.Sleep object at ...>]

  >>> for s in office_subscriptions: s.do()
  Martijn is sleeping at Grok corp(r)(tm) headquarters.

"""  # noqa: E501 line too long

from zope import interface

import grokcore.component as grok


class Office(grok.Context):

    def __init__(self, name):
        self.name = name


# All caves are a kind of office.
class Cave(Office):
    pass


class Mammoth(grok.Context):

    def __init__(self, name):
        self.name = name


class IActivity(interface.Interface):

    def do():
        """Do something."""


@grok.implementer(IActivity)
class Sleep(grok.MultiSubscription):
    grok.adapts(Office, Mammoth)

    def __init__(self, where, who):
        self.where = where
        self.who = who

    def do(self):
        print(f'{self.who.name} is sleeping at {self.where.name}.')


@grok.implementer(IActivity)
class DayTimeActivity(grok.MultiSubscription):
    grok.adapts(Cave, Mammoth)
    grok.baseclass()

    def __init__(self, where, who):
        self.where = where
        self.who = who

    def do(self):
        print('nothing')


class Food(DayTimeActivity):

    def do(self):
        print(f'{self.who.name} is feeding himself at {self.where.name}.')


class WritingCode(DayTimeActivity):

    def do(self):
        print(f'{self.who.name} is writing code at {self.where.name}!')
