"""
  >>> grok.testing.grok(__name__)

  >>> IMarker.providedBy(not_marked)
  False
  >>> IMarker.providedBy(marked)
  True
  >>> IMarker.providedBy(double_marked)
  True

  >>> IMarker2.providedBy(not_marked)
  False
  >>> IMarker2.providedBy(marked)
  False
  >>> IMarker2.providedBy(double_marked)
  True

  >>> marked()
  123

  >>> double_marked()
  234

"""

from zope import interface

import grokcore.component as grok


class IMarker(interface.Interface):
    pass


class IMarker2(interface.Interface):
    pass


@grok.provider(IMarker)
def marked():
    return 123


@grok.provider(IMarker, IMarker2)
def double_marked():
    return 234


def not_marked():
    return 456
