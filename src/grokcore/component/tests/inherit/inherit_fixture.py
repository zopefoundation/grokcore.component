from zope.interface import Interface

import grokcore.component


class Foo(grokcore.component.Context):
    pass


grokcore.component.context(Foo)


class IAnder(Interface):
    pass


class FooAdapter(grokcore.component.Adapter):
    grokcore.component.provides(IAnder)
