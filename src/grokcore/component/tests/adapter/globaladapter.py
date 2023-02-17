"""
  >>> grok.testing.grok(__name__)
  >>> from zope.component import getAdapter, getMultiAdapter

  >>> cave = Cave()
  >>> fireplace = Fireplace()

  >>> home = IHome(cave)
  >>> home.id
  'one'

  >>> home = getAdapter(cave, IHome, name="two")
  >>> home.id
  'two'

  >>> home = getAdapter(cave, IHome, name="three")
  >>> home.id
  'three'

  >>> home = getAdapter(cave, IHome, name="four")
  >>> home.id
  'four'

  >>> home = getAdapter(fireplace, IHome, name="five")
  >>> home.id
  'five'

  >>> home = getMultiAdapter((cave, fireplace), IHome)
  >>> home.id
  'six'

  >>> home = getAdapter(fireplace, IHome, name='seven')
  >>> home.id
  'seven-a'

  >>> home = getMultiAdapter((cave, fireplace), IHome, name='seven')
  >>> home.id
  'seven-b'

  >>> garage = getAdapter(cave, IGarage, name='named_garage_factory_name')
  >>> garage.id
  "I'm a garage"

  >>> garage = getAdapter(cave, IGarage)
  >>> garage.id
  "I'm a garage"

"""

from zope import interface
from zope.interface import implementer

import grokcore.component as grok


class Cave(grok.Context):
    pass


class Fireplace:
    pass


class IHome(interface.Interface):
    pass


@grok.implementer(IHome)
class Home:

    def __init__(self, id):
        self.id = id


@grok.implementer(IHome)
class CaveHomeFactory:

    def __init__(self, id):
        self.id = id

    def __call__(self, context):
        return Home(self.id)


class CaveFireplaceHomeFactory:

    def __init__(self, id):
        self.id = id

    def __call__(self, cave, fireplace):
        return Home(self.id)


factory1 = CaveHomeFactory("one")
factory2 = CaveHomeFactory("two")
factory3 = CaveHomeFactory("three")
factory4 = CaveHomeFactory("four")
factory5 = CaveHomeFactory("five")
factory6 = CaveFireplaceHomeFactory("six")
factory7a = CaveHomeFactory("seven-a")
factory7b = CaveFireplaceHomeFactory("seven-b")

# make some direct assertions

implementer(IHome)(factory3)
implementer(IHome)(factory4)
implementer(IHome)(factory5)
implementer(IHome)(factory6)
implementer(IHome)(factory7a)
implementer(IHome)(factory7b)

grok.adapter(Fireplace)(factory5)
grok.adapter(Fireplace)(factory7a)
grok.adapter(Cave, Fireplace)(factory7b)

# should accept single value for adapts
grok.global_adapter(factory1, Cave, IHome)
# should accept tuple for adapts
grok.global_adapter(factory2, (Cave,), IHome, name="two")
# should look at the provided interface
grok.global_adapter(factory3, Cave, name="three")
# should pick the canonical context
grok.global_adapter(factory4, name="four")
# should use __component_adapts__
grok.global_adapter(factory5, name="five")
# should work as multi-adapter
grok.global_adapter(factory6, (Cave, Fireplace,))
# should use __component_adapts__ adapting one object
grok.global_adapter(factory7a, name="seven")
# should use __component_adapts__ adaping two objects
grok.global_adapter(factory7b, name="seven")


class IGarage(interface.Interface):
    pass


@grok.implementer(IGarage)
class NamedGarageFactory:
    grok.name('named_garage_factory_name')

    def __init__(self, context):
        self.id = "I'm a garage"


implementer(IGarage)(NamedGarageFactory)

# should register a named adapter
grok.global_adapter(NamedGarageFactory, Cave, IGarage)
# should override component's name
grok.global_adapter(NamedGarageFactory, Cave, IGarage, name='')
