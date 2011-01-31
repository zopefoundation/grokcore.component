"""
  >>> grok.testing.grok(__name__)

  >>> cave = Cave('sweet home')

  >>> subscribers = grok.querySubscriptions(cave, IActivity)
  >>> subscribers
  [<grokcore.component.tests.subscriber.decorator.DebuggingGrokcore object at ...>]

  Subscripotion adapters are not registered as regular adapters:

  >>> component.queryAdapter(cave, IActivity)

"""


import grokcore.component as grok
from zope import interface, component


class Cave(grok.Context):

    def __init__(self, name):
        self.name = name

class IActivity(interface.Interface):
    pass


class DebuggingGrokcore(object):

    def __init__(self, where):
        self.where = where


@grok.subscribe(Cave)
@grok.implementer(IActivity)
def debugging(content):
    return DebuggingGrokcore(content)
