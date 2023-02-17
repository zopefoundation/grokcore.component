"""
  >>> grok.testing.grok(__name__)

  >>> cave = Cave('sweet home')

  >>> subscriptions = grok.querySubscriptions(cave, IActivity)
  >>> subscriptions
  [<grokcore.component.tests.subscriptions.decorator.DebuggingGrokcore object at ...>]

  Subscription adapters are not registered as regular adapters:

  >>> from zope import component
  >>> component.queryAdapter(cave, IActivity)

"""  # noqa: E501 line too long


from zope import interface

import grokcore.component as grok


class Cave(grok.Context):

    def __init__(self, name):
        self.name = name


class IActivity(interface.Interface):
    pass


class DebuggingGrokcore:

    def __init__(self, where):
        self.where = where


@grok.subscribe(Cave)
@grok.implementer(IActivity)
def debugging(content):
    return DebuggingGrokcore(content)
