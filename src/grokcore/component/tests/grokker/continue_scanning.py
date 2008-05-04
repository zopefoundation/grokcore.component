"""
A Grokker can declare that scanning should continue, so that other Grokkers can
still perform actions on the grokked components.

Here we define AlphaGrokker which has higher priority than BetaGrokker but does
not block BetaGrokker from picking up the same component::

    >>> grok.testing.grok(__name__)

In the fixture there is AlphaBetaSub that inherits from both Alpha and Beta.
Thus, both Grokkers are executed, with AlphaGrokker coming before BetaGrokker::

    >>> grok.testing.grok('grokcore.component.tests.grokker.continue_scanning_fixture')
    alpha
    beta

"""
import grokcore.component as grok


class Alpha(object):
    pass

class Beta(object):
    pass

class AlphaGrokker(grok.ClassGrokker):
    component_class = Alpha
    priority = 1 # we need to go before BetaGrokker

    def grok(self, name, factory, module_info, config, **kw):
        print "alpha"
        return True

class BetaGrokker(grok.ClassGrokker):
    component_class = Beta

    def grok(self, name, factory, module_info, config, **kw):
        print "beta"
        return True
    