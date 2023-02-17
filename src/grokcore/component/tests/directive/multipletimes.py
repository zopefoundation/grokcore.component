"""
Since grok.global_utility is a MultipleTimesDirective, there is a list of
GlobalUtilityInfo objects annotated on the module.


  >>> from martian import scan
  >>> import grokcore.component as grok
  >>> from grokcore.component.tests.directive import multipletimes
  >>> guis = grok.global_utility.bind().get(multipletimes)
  >>> len(guis)
  2

  >>> factory, provides, name, direct = guis[0]
  >>> factory
  <class 'grokcore.component.tests.directive.multipletimes.Club'>
  >>> provides
  <InterfaceClass grokcore.component.tests.directive.multipletimes.IClub>
  >>> name
  'foo'

  >>> factory, provides, name, direct = guis[1]
  >>> factory
  <class 'grokcore.component.tests.directive.multipletimes.Cave'>
  >>> provides is None
  True
  >>> name
  ''

"""
from zope import interface

import grokcore.component as grok


class IClub(interface.Interface):
    pass


class ICave(interface.Interface):
    pass


@grok.implementer(IClub)
class Club:
    pass


@grok.implementer(ICave)
class Cave:
    pass


grok.global_utility(Club, provides=IClub, name='foo')
grok.global_utility(Cave)
