from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('README.rst')
    + '\n' +
    read('CHANGES.rst')
)

tests_require = [
    'zope.event',
]

setup(
    name='grokcore.component',
    version='3.1',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://grok.zope.org',
    download_url='https://github.com/zopefoundation/grokcore.component',
    description='Grok-like configuration for basic components '
                '(adapters, utilities, subscribers)',
    long_description=long_description,
    license='ZPL',
    classifiers=['Intended Audience :: Developers',
                 'Development Status :: 6 - Mature',
                 'License :: OSI Approved :: Zope Public License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 ],

    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools',
                      'martian >= 1.2',
                      'zope.component',
                      'zope.configuration',
                      'zope.interface',
                      # Note: zope.testing is NOT just a test dependency here.
                      'zope.testing',
                      ],
    test_suite='grokcore.component.tests.test_grok.test_suite',
    tests_require=tests_require,
    extras_require={'test': tests_require},
)
