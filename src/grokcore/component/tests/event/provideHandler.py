"""
When you use the @grokcore.component.subscribe decorator, you can also
use zope.component.provideHandler to register the subscriber.  This
can be useful for unittests where you may not want to grok everything
in a module but just enable certain components.

  >>> from zope.interface.interfaces import ObjectEvent
  >>> from zope.component import provideHandler
  >>> provideHandler(mammothAdded)

  >>> manfred = Mammoth('Manfred')
  >>> import zope.event
  >>> zope.event.notify(ObjectEvent(manfred))
  >>> mammoths
  ['Manfred']

"""
from zope.interface.interfaces import IObjectEvent

import grokcore.component as grok


class Mammoth:
    def __init__(self, name):
        self.name = name


mammoths = []


@grok.subscribe(Mammoth, IObjectEvent)
def mammothAdded(mammoth, event):
    mammoths.append(mammoth.name)
