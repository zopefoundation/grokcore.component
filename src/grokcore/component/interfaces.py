from zope.interface import Interface

class IContext(Interface):
    """Marker interface for auto-association of context.

    The ``grok.context()`` directive is used to associate adapters with the
    class or interface they adapt. If there is only a single possible context
    object to adapt to in a module, you can leave out this directive and
    let the adapter associate automatically.

    If you want to make an object to be a candidate for this automatic
    association, you can subclass from ``grokcore.component.Context``.
    This implements this ``IContext`` directive.

    In some cases, you don't want to mix in a base class. You can instead
    mark up your class with ``zope.interface.implements(IContext)`` to make
    it a candidate for auto-association.
    """
