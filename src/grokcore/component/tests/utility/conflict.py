"""
Trying to register two utilities for the same interface (and
potentially under the same name) will generate a configuration
conflict:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
  ...
  ConfigurationConflictError: Conflicting configuration actions
    For: ('utility', <InterfaceClass grokcore.component.tests.utility.conflict.IUtilityInterface>, 'class and module')
  <BLANKLINE>
  <BLANKLINE>
    For: ('utility', <InterfaceClass grokcore.component.tests.utility.conflict.IUtilityInterface>, 'direct class')
  <BLANKLINE>
  <BLANKLINE>
    For: ('utility', <InterfaceClass grokcore.component.tests.utility.conflict.IUtilityInterface>, 'explicit class')
  <BLANKLINE>
  <BLANKLINE>
    For: ('utility', <InterfaceClass grokcore.component.tests.utility.conflict.IUtilityInterface>, 'implicit class')
  <BLANKLINE>
  <BLANKLINE>
    For: ('utility', <InterfaceClass grokcore.component.tests.utility.conflict.IUtilityInterface>, 'mixed class')
  <BLANKLINE>
  <BLANKLINE>

"""  # noqa: E501 line too long
from zope.interface import Interface
from zope.interface import provider

import grokcore.component as grok


class IUtilityInterface(Interface):
    pass


class IAnotherInterface(Interface):
    pass


@grok.implementer(IUtilityInterface)
class Implicit1(grok.GlobalUtility):
    grok.name('implicit class')


@grok.implementer(IUtilityInterface)
class Implicit2(grok.GlobalUtility):
    grok.name('implicit class')


@grok.implementer(IUtilityInterface, IAnotherInterface)
class Explicit1(grok.GlobalUtility):
    grok.provides(IUtilityInterface)
    grok.name('explicit class')


@grok.implementer(IUtilityInterface, IAnotherInterface)
class Explicit2(grok.GlobalUtility):
    grok.provides(IUtilityInterface)
    grok.name('explicit class')


@grok.implementer(IUtilityInterface, IAnotherInterface)
class Mixed1(grok.GlobalUtility):
    grok.provides(IUtilityInterface)
    grok.name('mixed class')


@grok.implementer(IUtilityInterface)
class Mixed2(grok.GlobalUtility):
    grok.name('mixed class')


@provider(IUtilityInterface)
class Direct1(grok.GlobalUtility):
    grok.name('direct class')
    grok.direct()


@provider(IUtilityInterface)
class Direct2(grok.GlobalUtility):
    grok.name('direct class')
    grok.direct()


@grok.implementer(IUtilityInterface)
class ClassLevel(grok.GlobalUtility):
    """This utility inherits from Grok's base class and is registered
    this way."""
    grok.name('class and module')


@grok.implementer(IUtilityInterface)
class ModuleLevel:
    """This utility doesn't inherit from Grok's base class and is
    registered explicitly using the module-level directive below."""


grok.global_utility(ModuleLevel, name='class and module')
