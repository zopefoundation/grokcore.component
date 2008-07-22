from zope.interface import Interface, Attribute

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


class IBaseClasses(Interface):

    ClassGrokker = Attribute("Base class to define a class grokker.")
    InstanceGrokker = Attribute("Base class to define an instance grokker.")
    GlobalGrokker = Attribute("Base class to define a module grokker.")

    Context = Attribute("Base class for automatically associated contexts.")
 
    Adapter = Attribute("Base class for adapters.")
    MultiAdapter = Attribute("Base class for multi-adapters.")
    GlobalUtility = Attribute("Base class for global utilities.")


class IDirectives(Interface):

    def baseclass():
        """Mark this class as a base class.

        This means it won't be grokked, though if it's a possible context,
        it can still serve as a context.
        """

    def implements(*interfaces):
        """Declare that a class implements the given interfaces."""

    def adapts(*classes_or_interfaces):
        """Declare that a class adapts objects of the given classes or
        interfaces."""

    def context(class_or_interface):
        """Declare the context for views, adapters, etc.

        This directive can be used on module and class level.  When
        used on module level, it will set the context for all views,
        adapters, etc. in that module.  When used on class level, it
        will set the context for that particular class."""

    def name(name):
        """Declare the name of a view or adapter/multi-adapter.

        This directive can only be used on class level."""

    def provides(interface):
        """Explicitly specify with which interface a component will be
        looked up."""

    def global_utility(factory, provides=None, name=u''):
        """Register a global utility.

        factory - the factory that creates the global utility
        provides - the interface the utility should be looked up with
        name - the name of the utility
        """

    def direct():
        """Specify whether the class should be used for the component
        or whether it should be used to instantiate the component.

        This directive can be used on GlobalUtility-based classes to
        indicate whether the class itself should be registered as a
        utility, or an instance of it.
        """


class IDecorators(Interface):

    def subscribe(*classes_or_interfaces):
        """Declare that a function subscribes to an event or a
        combination of objects and events."""

    def adapter(*classes_or_interfaces):
        """Describes that a function adapts an object or a combination
        of objects.
        """

    def implementer(*interfaces):
        """Describes that a function that's used as an adapter
        implements an interface or a number of interfaces.
        """


class IGrokErrors(Interface):

    def GrokError(message, component):
        """Error indicating that a problem occurrend during the
        grokking of a module (at "grok time")."""

    def GrokImportError(*args):
        """Error indicating a problem at import time."""


class IMartianAPI(Interface):
    """Part of Martian's API exposed by grokcore.component."""

    # This should probably move to martian at some point.

    ClassGrokker = Attribute("Grokker for classes.")
    InstanceGrokker = Attribute("Grokker for instances.")
    GlobalGrokker = Attribute("Grokker that's invoked for a module.")


class IGrokcoreComponentAPI(IBaseClasses, IDirectives, IDecorators,
                            IGrokErrors, IMartianAPI):
    """grokcore.component's public API."""
