"""
It raises ConflictError if ZCML and grok try to register an adapter from/to
the same classes.

>>> xmlconfig.string('''
...     <configure
...         xmlns="http://namespaces.zope.org/zope"
...         xmlns:grok="http://namespaces.zope.org/grok">
...       <include package="zope.component" file="meta.zcml"/>
...       <include package="grokcore.component" file="meta.zcml"/>
...       <adapter factory=".fixture.ZCMLHome" />
...       <grok:grok package="." />
...     </configure>''', context)
Traceback (most recent call last):
ConfigurationConflictError: ...

"""

from zope.configuration import xmlconfig

from grokcore.component.tests.zcml import conflictpkg


context = xmlconfig.ConfigurationMachine()
xmlconfig.registerCommonDirectives(context)
context.package = conflictpkg
