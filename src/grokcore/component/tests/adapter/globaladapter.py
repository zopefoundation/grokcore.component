"""
  >>> grok.testing.grok(__name__)
  >>> from zope.component import getAdapter, getMultiAdapter
  
  >>> cave = Cave()
  >>> fireplace = Fireplace()
  
  >>> home = IHome(cave)
  >>> home.id
  u'one'
  
  >>> home = getAdapter(cave, IHome, name=u"two")
  >>> home.id
  u'two'
  
  >>> home = getAdapter(cave, IHome, name=u"three")
  >>> home.id
  u'three'
  
  >>> home = getAdapter(cave, IHome, name=u"four")
  >>> home.id
  u'four'
  
  >>> home = getAdapter(fireplace, IHome, name=u"five")
  >>> home.id
  u'five'
  
  >>> home = getMultiAdapter((cave, fireplace), IHome)
  >>> home.id
  u'six'
  
"""

import grokcore.component as grok
from zope import interface

class Cave(grok.Context):
    pass

class Fireplace(object):
    pass

class IHome(interface.Interface):
    pass

class Home(object):
    grok.implements(IHome)
    
    def __init__(self, id):
        self.id = id

class CaveHomeFactory(object):
    grok.implements(IHome)
    
    def __init__(self, id):
        self.id = id
    
    def __call__(self, context):
        return Home(self.id)

class CaveFireplaceHomeFactory(object):
    def __init__(self, id):
        self.id = id
    
    def __call__(self, cave, fireplace):
        return Home(self.id)

factory1 = CaveHomeFactory(u"one")
factory2 = CaveHomeFactory(u"two")
factory3 = CaveHomeFactory(u"three")
factory4 = CaveHomeFactory(u"four")
factory5 = CaveHomeFactory(u"five")
factory6 = CaveFireplaceHomeFactory(u"six")

# make some direct assertions

grok.implementer(IHome)(factory3)
grok.implementer(IHome)(factory4)
grok.implementer(IHome)(factory5)
grok.implementer(IHome)(factory6)

grok.adapter(Fireplace)(factory5)

grok.global_adapter(factory1, Cave, IHome)                  # should accept single value for adapts
grok.global_adapter(factory2, (Cave,), IHome, name="two")   # should accept tuple for adapts
grok.global_adapter(factory3, Cave, name="three")           # should look at the provided interface
grok.global_adapter(factory4, name=u"four")                 # should pick the canonical context
grok.global_adapter(factory5, name="five")                  # should use __component_adapts__
grok.global_adapter(factory6, (Cave, Fireplace,))           # should work as multi-adapter
