grokcore.component
******************

This module packages,
separately from the mainline ``grok`` web framework module itself,
the component auto-configuration tools
that let Grok programmers avoid writing ZCML.
With this module,
basic Zope components like adapters and utilities can be written
and then registered by providing Grok directives,
instead of having to write ZCML.
