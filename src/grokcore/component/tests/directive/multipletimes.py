"""
Since grok.global_utility is a MultipleTimesDirective, there is a list of
GlobalUtilityInfo objects annotated on the module.


  >>> from martian import scan
  >>> import grokcore.component as grok
  >>> from grokcore.component.tests.directive import multipletimes
  >>> guis = grok.global_utility.get(multipletimes)
  >>> guis
  [<grokcore.component.directive.GlobalUtilityInfo object at 0x...>,
  <grokcore.component.directive.GlobalUtilityInfo object at 0x...>]
  >>> guis[0].factory
  <class 'grokcore.component.tests.directive.multipletimes.Club'>
  >>> guis[0].provides
  <InterfaceClass grokcore.component.tests.directive.multipletimes.IClub>
  >>> guis[0].name
  'foo'
  >>> guis[1].factory
  <class 'grokcore.component.tests.directive.multipletimes.Cave'>
  >>> guis[1].provides is None
  True
  >>> guis[1].name
  u''

"""
import grokcore.component as grok
from zope import interface

class IClub(interface.Interface):
    pass

class ICave(interface.Interface):
    pass

class Club(object):
    grok.implements(IClub)

class Cave(object):
    grok.implements(ICave)

grok.global_utility(Club, provides=IClub, name='foo')
grok.global_utility(Cave)
