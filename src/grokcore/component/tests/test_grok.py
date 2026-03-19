import doctest
import traceback
import unittest
from importlib.resources import files

import zope.component.eventtesting
from zope.testing import cleanup


def setUpZope(test):
    zope.component.eventtesting.setUp(test)


def cleanUpZope(test):
    cleanup.cleanUp()


def suiteFromPackage(name):
    test_dir = files('grokcore.component.tests').joinpath(name)
    file_list = [f.name for f in test_dir.iterdir() if f.name.endswith('.py')]
    suite = unittest.TestSuite()
    for filename in file_list:
        if filename.endswith('_fixture.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = f'grokcore.component.tests.{name}.{filename[:-3]}'
        try:
            test = doctest.DocTestSuite(
                dottedname,
                setUp=setUpZope,
                tearDown=cleanUpZope,
                optionflags=doctest.ELLIPSIS
                | doctest.NORMALIZE_WHITESPACE
                | doctest.IGNORE_EXCEPTION_DETAIL)
        except ModuleNotFoundError:  # or should this accept anything?
            traceback.print_exc()
            raise
        suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in ['adapter', 'directive', 'grokker', 'utility', 'view',
                 'event', 'inherit', 'order', 'subscriptions', 'zcml']:
        suite.addTest(suiteFromPackage(name))

    api = doctest.DocFileSuite('api.txt')
    suite.addTest(api)

    # this test cannot follow the normal testing pattern, as the
    # bug it tests for is only exposed in the context of a doctest
    grok_component = doctest.DocFileSuite('grok_component.txt',
                                          setUp=setUpZope,
                                          tearDown=cleanUpZope)
    suite.addTest(grok_component)
    return suite
