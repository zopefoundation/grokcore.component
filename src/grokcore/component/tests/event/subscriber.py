"""
You can subscribe to events using the @grok.subscribe decorator:

  >>> import zope.event
  >>> from zope.interface.interfaces import ObjectEvent
  >>> grok.testing.grok(__name__)
  >>> manfred = Mammoth('Manfred')
  >>> zope.event.notify(ObjectEvent(manfred))
  >>> mammoths
  ['Manfred']
  >>> mammoths2
  ['Manfred']

The decorated event handling function can also be called directly:

  >>> mammothAdded(Mammoth('Max'),None)
  >>> mammoths
  ['Manfred', 'Max']

"""

from zope.interface.interfaces import IObjectEvent

import grokcore.component as grok


class Mammoth:
    def __init__(self, name):
        self.name = name


mammoths = []
mammoths2 = []


@grok.subscribe(Mammoth, IObjectEvent)
def mammothAdded(mammoth, event):
    mammoths.append(mammoth.name)


@grok.subscribe(Mammoth, IObjectEvent)
def mammothAddedInstance(mammoth, event):
    mammoths2.append(mammoth.name)
