"""
>>> grok.testing.grok('grokcore.component.tests.adapter.adapter')

You can't call grok.context from a function:

  >>> func()
  Traceback (most recent call last):
    ...
  GrokImportError: The 'context' directive can only be used on class or
  module level.

You can't call grok.context from a method either:

  >>> SomeClass().meth()
  Traceback (most recent call last):
    ...
  GrokImportError: The 'context' directive can only be used on class or
  module level.

"""
import grokcore.component as grok
from grokcore.component.tests.adapter.adapter import Cave


def func():
    """We don't allow calling `grok.context` from anything else than a
    module or a class"""
    grok.context(Cave)


class SomeClass:

    def meth(self):
        """We don't allow calling `grok.context` from anything else
        than a module or a class"""
        grok.context(Cave)
