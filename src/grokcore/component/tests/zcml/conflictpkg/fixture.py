from zope import component
from zope import interface

import grokcore.component as grok


class Cave(grok.Context):
    pass


class IHome(interface.Interface):
    pass


@grok.implementer(IHome)
class GrokHome(grok.Adapter):
    pass


@component.adapter(Cave)
@interface.implementer(IHome)
class ZCMLHome:
    pass
