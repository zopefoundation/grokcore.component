"""
If no model can be found in the module, we get an error:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: No module-level context for
  <class 'grokcore.component.tests.adapter.nomodel.Home'>, please use the
  'context' directive.

"""
from zope import interface

import grokcore.component as grok


class IHome(interface.Interface):
    pass


@grok.implementer(IHome)
class Home(grok.Adapter):
    pass
