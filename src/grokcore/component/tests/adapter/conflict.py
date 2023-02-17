"""
Registering two adapters for the same target interface should provoke
a conflict, even if the interface is guessed (instead of being
explicitly declared with grok.provides):

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
  ...
  ConfigurationConflictError: Conflicting configuration actions
    For: ('adapter', <InterfaceClass grokcore.component.tests.adapter.conflict.ICave>, <InterfaceClass grokcore.component.tests.adapter.conflict.IDecoration>, u'')

"""  # noqa: E501 line too long
from zope.interface import Interface

import grokcore.component as grok


class ICave(Interface):
    pass


class IDecoration(Interface):
    pass


class ICaveCleaning(Interface):
    pass


@grok.implementer(ICave)
class Cave:
    pass


@grok.implementer(IDecoration)
class ImplicitProvides(grok.Adapter):
    """Here the provided interface is guessed because the class only
    implements one interface."""
    grok.context(ICave)


@grok.implementer(IDecoration, ICaveCleaning)
class ExplicitProvides(grok.Adapter):
    """Here the provided interface is specific explicitly."""
    grok.context(ICave)
    grok.provides(IDecoration)
