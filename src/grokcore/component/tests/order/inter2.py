"""
This module used by inter1 tests
"""

import grokcore.component as grok


class Four:
    grok.order(1)


class Five:
    pass


class Six:
    grok.order()
