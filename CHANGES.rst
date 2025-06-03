Changes
=======

4.2 (2025-06-03)
----------------

* Add support for Python 3.12, 3.13.

* Drop support for Python 3.7, 3.8.


4.1.1 (2025-01-28)
------------------

- Adjust discriminator for adapters so it matches the one used by the
  ``zope.component`` ZCML directive (``<adapter factory=""/>``) and thus a
  conflict error is raised if there are two registrations for the same
  discriminator.


4.1 (2023-03-21)
----------------

- Upgrade to support ``zope.interface >= 6.0`` by no longer importing removed
  functions:

    + ``classProvides``
    + ``implementsOnly``


4.0 (2023-02-17)
----------------

- Add support for Python 3.10, 3.11.

- Drop support for Python 2.7, 3.5, 3.6.


3.2.0 (2021-03-22)
------------------

- Add support for Python 3.7 up to 3.9.

- Update to ``zope.component >= 5``.

- Drop support for Python 3.4.


3.1 (2018-05-09)
----------------

- Expose ``martian.ignore`` through our API.

3.0.2 (2018-01-17)
------------------

- Replace the use of `grok.implements()` with the `@grok.implementer()`
  directive throughout.

3.0.1 (2018-01-12)
------------------

- Rearrange tests such that Travis CI can pick up all functional tests too.

3.0 (2017-10-19)
----------------

- Add support for Python 3.5, 3.6, PyPy2 and PyPy3.

- Drop support for Python 2.6 and 3.3.

2.7 (2016-02-16)
----------------

- Add ability to exclude more than one module or package using
  ``<grok:grok exclude="<names>" />`` and allow to use unix shell-style
  wildcards within.

2.6.1 (2016-01-29)
------------------

- Make grokcore.component.implementer compatible with
  zope.interface.implementer by allowing doing the adapter magic when
  used on functions.

2.6 (2015-05-12)
----------------

- Compatibility for python 3l

- Python 3 doesn't support the directive ``zope.interface.implements``
  any more and is required to use the ``@implementer`` class decorator instead.
  This version of grokcore.components provides its own
  ``grokcore.component.implements`` directive for both Python 2 and 3.
  So this directive can still be used with the help of a grokker.
  If you use grokcore.components >= 2.6  the new implementation will be used
  while earlier versions used zope.interface.implements.

2.5 (2012-05-01)
----------------

- Introduce provideUtility, providerAdapter, provideSubscriptionAdapter,
  provideHandler and provideInterface in grokcore.component. These by default
  delegate the registration of components to the global site manager like
  was done before, but provide the possibility for custom registries for the
  grokked components.

- Fix the `global_adapter` to properly use information annotated by
  ``grok.adapter``, and using the IContext object if it was not
  specified. (Fix Launchpad issue #960097).

- Add a ``key`` option to ``sort_components`` that behave like ``key``
  options available on standard Python sort methods.

2.4 (2011-04-27)
----------------

- Fix the `global_adapter` directive implementation to accept an explicit
  "empty" name for nameless adapter registrations (as it used to be that
  providing an empty name in the registration would actually result in
  registering a named adapter in case the factory has a `grok.name`).

2.3 (2011-02-14)
----------------

- Implement the generic (Multi)Subscriptions components.

2.2 (2010-11-03)
----------------

- The default values computation for the context directive and the provides
  directive is now defined in the directives themselves. This means that where
  the values for these directives is being retrieved, the "default_context"
  function does not need to be passed along anymore for general cases.

  Analogous to this, when getting values for the provides directive the
  "default_provides" function does not need to be passed along in the general
  case.

2.1 (2010-11-01)
----------------

* Made package comply to zope.org repository policy.

* Moved directives 'order' from grokcore.viewlet and 'path' from
  grokcore.view to this very package.

* Tiny dependency adjustment: moved zope.event to test dependencies.

* Port from 1.x branch exclude parameter to the Grok ZCML directive.

* Port from 1.x branch the ignore of testing.py modules.

2.0 (2009-09-16)
----------------

* Use a newer version of Martian that has better support for
  inheritance.  This is demonstrated in ``tests/inherit``.

* The ``ContextGrokker`` and the ``scan.py`` module have gone away
  thanks the newer Martian.

* Directive implementations (in their factory method) should *not*
  bind directives. Directive binding cannot take place at import time,
  but only at grok time. Binding directives during import time (when
  directives are executed) can lead to change problems. (we noticed
  this during our refactoring to use the new Martian).

* Use 1.0b1 versions.cfg in Grok's release info instead of a local
  copy; a local copy for all grokcore packages is just too hard to
  maintain.

1.7 (2009-06-01)
----------------

* Add missing provider, global_adapter, implementsOnly, classProvides() to
  the module interface so that they are included in __all__

1.6 (2009-04-10)
----------------

* Add convenience imports for implementsOnly() and classProvides() class
  declarations form zope.interface.

* Add support for registering global adapters at module level::

    grok.global_adapter(factory, (IAdapted1, IAdapted2,), IProvided, name=u"name")

  Only 'factory' is required. If only a single interface is adapted, the
  second argument may be a single interface instead of a tuple. If the
  component has declared adapted/provided interfaces, the second and third
  arguments may be omitted.

* Add support for an @provider decorator to let a function directly provide
  an interface::

    @grok.provider(IFoo, IBar)
    def some_function():
        ...

  This is equivalent to doing alsoProvides(some_function, IFoo, IBar).

* Add support for named adapters with the @adapter decorator::

    @grok.adapter(IAdaptedOne, IAdaptedTwo, name=u"foo")
    def some_function(one, two):
        ...

1.5.1 (2008-07-28)
------------------

* The ``IGrokcoreComponentAPI`` interface was missing declarations for
  the ``title`` and ``description`` directives.

1.5 (2008-07-22)
----------------

* Fix https://bugs.launchpad.net/grok/+bug/242353: grokcore.component
  contains old-style test setup. There is no `register_all_tests`
  method in grokcore.component.testing anymore. Use z3c.testsetup
  instead.

* Allow functions that have been marked with @grok.subscribe also be
  registered with ``zope.component.provideHandler()`` manually.  This
  is useful for unit tests where you may not want to grok a whole
  module.

* Document grokcore.component's public API in an interface,
  ``IGrokcoreComponentAPI``.  When you now do::

    from grokcore.component import *

  only the items documented in that interface will be imported into
  your local namespace.

1.4 (2008-06-11)
----------------

* Ported class grokkers to make use of further improvements in Martian.
  This requires Martian 0.10.

1.3 (2008-05-14)
----------------

* Ported class grokkers to make use of the new declarative way of
  retrieving directive information from a class.  This requires
  Martian 0.9.6.

1.2.1 (2008-05-04)
------------------

* Upgrade to Martian 0.9.5, which has a slight change in the signature of
  ``scan_for_classes``.

* Remove an unnecessary import ``methods_from_class`` from
  ``grokcore.component.scan``.

1.2 (2008-05-04)
----------------

* Ported directives to Martian's new directive implementation.  As a
  result, nearly all helper functions that were available from
  ``grokcore.component.util`` have been removed.  The functionality is
  mostly available from the directives themselves now.

* The ``baseclass`` directive has been moved to Martian.

* The ``order`` directive and its helper functions have been moved
  back to Grok, as it was of no general use, but very specific to
  viewlets.

1.1 (2008-05-03)
----------------

* ``determine_module_component`` now looks for classes that implement
  a certain interface (such as ``IContext``), instead of taking a list
  of classes.  If looking for ``IContext``, it still will find
  ``Context`` subclasses, as these were also made to implement
  ``IContext``.

* Move the ``public_methods_from_class`` helper function back to Grok,
  it isn't used at all in ``grokcore.component``.

1.0.1 (2008-05-02)
------------------

* The grokkers for adapters and global utilities did not use the
  correct value for the *provided* interface in the configuration
  action discriminator.  Because of this, uninformative and
  potentially wrong conflict errors would occur, as well as no
  conflict where a conflict should have occurred.

* The grokker for the ``global_utility()`` directive did immediate
  registrations instead of generating configuration actions.
  Therefore it did not provoke ``ConflictErrors`` for conflicting
  registrations.

* Improved documentation

1.0 (2008-05-01)
----------------

* Created ``grokcore.component`` in March 2008 by factoring basic
  component base classes and their directives and grokkers out of
  Grok.
