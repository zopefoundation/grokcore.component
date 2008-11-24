This package provides base classes of basic component types for the
Zope Component Architecture, as well as means for configuring and
registering them directly in Python (without ZCML).

.. contents::

How to set up ``grokcore.component``
====================================

In the following we assume you're writing or extending an application
that does bootstrap configuration using ZCML.  There's always a single
ZCML file that is executed when the application is started, which then
includes everything else.  Let's assume this file is called
``site.zcml`` (that's what it's called in Zope), so that file is what
we'll be editing.

In order to register the components that you wrote using the base
classes and directives available from ``grokcore.component``, we'll
use the ``<grok:grok />`` ZCML directive.  But before we can use it,
we need to make sure it's available to the ZCML machinery.  We do this
by including the meta configuration from ``grokcore.component``::

  <include package="grokcore.component" file="meta.zcml" />

Put this line somewhere to the top of ``site.zcml``, next to other
meta configuration includes.  Now, further down the line, we can tell
the machinery in ``grokcore.component`` to register all components in
your package (let's say it's called ``helloworld``)::

  <grok:grok package="helloworld" />

To sum up, your ``site.zcml`` file should look like something like this::

  <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:grok="http://namespaces.zope.org/grok">

    <!-- do the meta configuration to make the ZCML directives available -->
    <include package="zope.foobar" file="meta.zcml" />
    <include package="zope.frobnaz" file="meta.zcml" />
    <include package="grokcore.component" file="meta.zcml" />

    <!-- now load the configuration of packages that we depend on -->
    <include package="zope.barfoo" />
    <include package="zope.somethingorother" />

    <!-- finally load my components which are based on grokcore.component -->
    <grok:grok package="helloworld" />

  </configure>

Examples
========

Adapter
-------

Here's a simple adapter that may be useful in Zope.  It extracts the
languages that a user prefers from the request::

  import grokcore.component
  from zope.publisher.interfaces.browser import IBrowserRequest
  from zope.i18n.interfaces import IUserPreferredLanguages

  class CookieLanguage(grokcore.component.Adapter):
      """Extract the preferred language from a cookie"""
      grokcore.component.context(IBrowserRequest)
      grokcore.component.implements(IUserPreferredLanguages)

      # No need to implement __init__, it's already provided by the base class.

      def getPreferredLanguages(self):
          # This an adapter for the request, so self.context is the request.
          request = self.context

          # Extract the preferred language from a cookie:
          lang = request.cookies.get('language', 'en')

          # According to IUserPreferredLanguages, we must return a list.
          return [lang]

Multi-adapter
-------------

Here's a multi-adapter that functions as a content provider as known
from the ``zope.contentprovider`` library.  Content providers are
components that return snippets of HTML.  They're multi-adapters for
the content object (model), the request and the view that they're
supposed to be a part of::

  import grokcore.component
  from zope.publisher.interfaces.browser import IBrowserRequest
  from zope.publisher.interfaces.browser import IBrowserPage
  from zope.contentprovider.interfaces import IContentProvider

  class HelloWorldProvider(grokcore.component.MultiAdapter):
      """Display Hello World!"""
      grokcore.component.adapts(Interface, IBrowserRequest, IBrowserPage)
      grokcore.component.implements(IContentProvider)

      def update(self):
          pass

      def render(self):
          return u'<p>Hello World!</p>'


Global utility
--------------

Here's a simple named utility, again from the Zope world.  It's a
translation domain.  In other words, it contains translations of user
messages and is invoked when the i18n machinery needs to translate
something::

  import grokcore.component
  from zope.i18n.interfaces import ITranslationDomain

  class HelloWorldTranslationDomain(grokcore.component.GlobalUtility):
      grokcore.component.implements(ITranslationDomain)
      grokcore.component.name('helloworld')

      domain = u'helloworld'

      def translate(self, msgid, mapping=None, context=None,
                    target_language=None, default=None):
          if target_language is None:
              preferred = IUserPreferredLanguages(context)
              target_language = preferred.getPreferredLanguages()[0]

          translations = {'de': u'Hallo Welt',
                          'nl': u'Hallo Wereld'}
          return translations.get(target_language, u'Hello World')

Of course, it's silly to implement your own translation domain utility
if there are already implementations available in ``zope.i18n`` (one
that reads translations from a GNU gettext message catalog and a
simple implementation for tests).  Let's try to reuse that
implementation and register an instance::

  import grokcore.component
  from zope.i18n.interfaces import ITranslationDomain
  from zope.i18n.simpletranslationdomain import SimpleTranslationDomain

  messages = {('de', u'Hello World'): u'Hallo Welt',
              ('nl', u'Hello World'): u'Hallo Wereld'}
  helloworld_domain = SimpleTranslationDomain(u'helloworld', messages)

  grokcore.component.global_utility(helloworld_domain,
                                    provides=ITranslationDomain,
                                    name='helloworld',
                                    direct=True)


Subscriber
----------

Here we see a subscriber much like it occurs within Zope itself.  It
subscribes to the modified event for all annotatable objects (in other
words, objects that can have metadata associated with them).  When
invoked, it updates the Dublin Core 'Modified' property accordingly::

  import datetime
  import grokcore.component
  from zope.annotation.interfaces import IAnnotatable
  from zope.lifecycleevent.interfaces import IObjectModifiedEvent
  from zope.dublincore.interfaces import IZopeDublinCore

  @grokcore.component.subscribe(IAnnotatable, IObjectModifiedEvent)
  def updateDublinCoreAfterModification(obj, event):
      """Updated the Dublin Core 'Modified' property when a modified
      event is sent for an object."""
      IZopeDublinCore(obj).modified = datetime.datetime.utcnow()


API overview
============

Base classes
------------

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
----------------------

``implements(iface1, iface2, ...)``
    declares that a class implements the interfaces ``iface1``,
    ``iface2``, etc.  It is identical to
    ``zope.interface.implements``.

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
-----------------------

``global_utility(class, [provides=iface, name=ascii_or_unicode, direct=bool])``
    registers an instance of ``class`` (or ``class`` itself, depending
    on the value of the ``direct`` parameter) as a global utility.
    This allows you to register global utilities that don't inherit
    from the ``GlobalUtility`` base class.


Function decorators
-------------------

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
