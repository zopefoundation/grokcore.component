"""
Subclasses of grok.GlobalUtility that implement more than one interface must
specify which interface to use for the registration:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grokcore.component.tests.utility.implementsmany.Club'> is implementing
  more than one interface (use grok.provides to specify which one to use).
"""
import grokcore.component as grok
from zope import interface

class IClub(interface.Interface):
    pass

class ISpikyClub(interface.Interface):
    pass

@grok.implementer(IClub, ISpikyClub)
class Club(grok.GlobalUtility):
    pass
