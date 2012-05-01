from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('CHANGES.txt')
    )

tests_require = [
    'zope.event',
    ]

setup(
    name='grokcore.component',
    version='2.5',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://grok.zope.org',
    download_url='http://pypi.python.org/pypi/grokcore.component',
    description='Grok-like configuration for basic components '
                '(adapters, utilities, subscribers)',
    long_description=long_description,
    license='ZPL',
    classifiers=['Intended Audience :: Developers',
                 'License :: OSI Approved :: Zope Public License',
                 'Programming Language :: Python',
                 ],

    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools',
                      'martian >= 0.14',
                      'zope.component',
                      'zope.configuration',
                      'zope.interface',
                      # Note: zope.testing is NOT just a test dependency here.
                      'zope.testing',
                      ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
)
