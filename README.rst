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

There is an optional ``exclude`` on the `grok` directive. It allows to specify
names of packages or modules that if encountered won't be grokked. These
names might contain unix shell-style wildcards.

`implementer()` versus `implements()`
=====================================

Note how the Python 3 compatibility brings a change in how the
`grokcore.component.implements()` *directive* works. When using this directive
you now have to make sure the component is grokkked, to have the underlying
mechanism to take effect.

Alternatively you could start to use the `grokcore.component.implementer()`
*class decorator* instead. This will do the same thing, but does not require
your component to be grokkked and still have your component declare it
implements the given interface.

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

      def __init__(self, context, request, view):
          pass

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

Global adapter
--------------

Sometimes, you may have an object that should be registered as an adapter
factory. It may have come from some other framework that configured that
adapter for you, say, or you may have a class that you instantiate many
times to get different variations on a particular adapter factory. In these
cases, subclassing grokcore.component.Adapter or MultiAdapter is not
possible. Instead, you can use the global_adapter() directive. Here is an
example drawing on the ``z3c.form`` library, which provides an adapter factory
factory for named widget attributes::

  import zope.interface
  import zope.schema
  import grokcore.component
  import z3c.form.widget import ComputedWidgetAttribute

  class ISchema(Interface):
      """This schema will be used to power a z3c.form form"""

      field = zope.schema.TextLine(title=u"Sample field")

  ...

  label_override = z3c.form.widget.StaticWidgetAttribute(
                        u"Override label", field=ISchema['field'])

  grokcore.component.global_adapter(label_override, name=u"label")

In the example above, the provided and adapted interfaces are deduced from the
object returned by the ``StaticWidgetAttribute`` factory. The full syntax
for global_adapter is::

  global_adapter(factory, (IAdapted1, IAdapted2,), IProvided, name=u"name")

The factory must be a callable (the adapter factory). Adapted interfaces are
given as a tuple. You may use a single interface instead of a one-element
tuple for single adapters. The provided interface is given as shown. The name
defaults to u"" (an unnamed adapter).

Handling events
---------------

Here we see an event handler much like it occurs within Zope itself. It
subscribes to the modified event for all annotatable objects (in other words,
objects that can have metadata associated with them). When invoked, it updates
the Dublin Core 'Modified' property accordingly::

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

Subscriptions
-------------

Subscriptions look similar to Adapter, however, unlike regular adapters,
subscription adapters are used when we want all of the adapters that adapt an
object to a particular adapter.

Analogous to MultiAdapter, there is a MultiSubscription component that "adapts"
multiple objects.
