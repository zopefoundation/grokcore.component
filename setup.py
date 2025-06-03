import os

from setuptools import find_packages
from setuptools import setup


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
    version='4.2',
    author='Grok Team',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/grokcore.component',
    description='Grok-like configuration for basic components '
                '(adapters, utilities, subscribers)',
    long_description=long_description,
    license='ZPL',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 6 - Mature',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
    install_requires=['setuptools',
                      'martian >= 1.2',
                      'zope.component',
                      'zope.configuration',
                      'zope.interface',
                      # Note: zope.testing is NOT just a test dependency here.
                      'zope.testing',
                      ],
    extras_require={'test': tests_require},
)
