"""
Subclasses of grok.GlobalUtility that are supposed to be registered
directly as utilities and which provide more than one interface must
specify which interface to use for the registration:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grokcore.component.tests.utility.providesmany2.Club'>
  provides more than one interface (use grok.provides to specify which one
  to use).
"""
from zope import interface

import grokcore.component as grok


class IClub(interface.Interface):
    pass


class ISpikyClub(interface.Interface):
    pass


@interface.provider(IClub, ISpikyClub)
class Club:
    pass


grok.global_utility(Club, direct=True)
