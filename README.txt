This package provides base classes of basic component types for the
Zope Component Architecture, as well as means for configuring and
registering them directly in Python (without ZCML).


Base classes
============

``Adapter``
    Base class for an adapter that adapts a single object (commonly
    referred to as the *context*).  Use the ``context`` directive to
    specify which object to adapt and the ``implements`` directive to
    specify which interface the adapter will provide.  If it's a named
    adapter, you may use the ``name`` directive to specify the name.

``MultiAdapter``
    Base class for an adapter that adapts *n* objects (where *n>=1*).
    Use the ``adapts`` directive to specify which kinds of objects are
    adapted and the ``implements`` directive to specify which
    interface the adapter will provide.  If it's a named
    multi-adapter, you may use the ``name`` directive to specify the
    name.

``GlobalUtility``
    Base class for a globally registered utility.  Unless you use the
    ``direct`` directive to indicate that the class itself should be
    registered as a utility, the class will automatically be
    instantiated, therefore the constructor may not take any
    arguments.  Use the ``implements`` directive to specify which
    interface the utility provides, or if that is not unambiguous,
    also use the ``provides`` directive to specify which of the
    implemented interfaces should be used when registering the
    utility.  If it's a named utility, you may use the ``name``
    directive to specify the name.

``Context``
    Subclasses of this will automatically be found as potential
    contexts for adapters and other types of context-dependent
    components.


Class-level directives
======================

``implements(iface1, iface2, ...)``
    declares that a class implements the interfaces ``iface1``,
    ``iface2``, etc.

``context(iface_or_class)``
    declares the type of object that the adapter (or a similar
    context-dependent component) adapts.  This can either be an
    interface (in this case all objects providing this interface will
    be eligible contexts for the adapter) or a class (then only
    instances of that particular class are eligible).

``adapts(iface_or_class1, iface_or_class_2, ...)``
    declares the types of objects that a multi-adapter adapts.

``name(ascii_or_unicode)``
    declares the name of a named utility, named adapter, etc.

``title(ascii_or_unicode)``
    declares the human-readable title of a component (such as a
    permission, role, etc.)

``provides(iface)``
    declares the interface that a utility provides (as opposed to
    potentially multiple interfaces that the class implements).

``direct()``
    declares that a ``GlobalUtility`` class should be registered as a
    utility itself, rather than an instance of it.

``baseclass()``
    declares that a subclass of an otherwise automatically configured
    component should not be registered, and that it serves as a base
    class instead.


Module-level directives
=======================

``global_utility(class, [provides=iface, name=ascii_or_unicode, direct=bool])``
    registers an instance of ``class`` (or ``class`` itself, depending
    on the value of the ``direct`` parameter) as a global utility.
    This allows you to register global utilities that don't inherit
    from the ``GlobalUtility`` base class.


Function decorators
===================

``@adapter(iface_or_class1, iface_or_class2, ...)``
    registers the function as an adapter for the specific interface.

``@implementer(iface_or_class1, iface_or_class2, ...)```
    declares that the function implements a certain interface (or a
    number of certain interfaces).  This is useful when a function
    serves as an object factory, e.g. as an adapter.

``@subscribe(iface_or_class1, iface_or_class2, ...)``
    declares that a function is to be registered as an event handler
    for the specified objects.  Normally, an event handler is simply
    registered as a subscriber for the event interface.  In case of
    object events, the event handler is registered as a subscriber for
    the object type and the event interface.
