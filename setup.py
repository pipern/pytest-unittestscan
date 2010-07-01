"""
py.test plugin to find unittest cases using the same method that
setuptools/setup.py uses.

Usage
---------------

Unfortunately, we can't ready setup.py very easily to determine
test_suites. So instead we'll read setup.cfg and get a list of places
to search for unittest tests from there. This means you have to edit
your project and copy some information from setup.py into setup.cfg.

We read setup.cfg like this:

[pytest_unittest]
scan = proj.tests:suite

In that example, we will import and run the suite() function to find
unittest TestSuite.

Another example:

[pytest_unittest]
scan = proj.test_dir

We will then import all *.py files found in
proj.test_dir and use any TestCase or TestSuite subclasses found.

"""

from setuptools import setup

setup(
    name="pytest-setuptools",
    version="0.1",
    description='py.test setuptools unittest plugin',
    long_description=__doc__,
    license='BSD',
    author='Nick Piper',
    author_email='nick.piper@logica.com',
    url='http://github.com/pipern/pytest-setuptools',
    platforms=['linux', 'osx', 'win32'],
    py_modules=['pytest_setuptools'],
    entry_points = {'pytest11': ['pytest_setuptools = pytest_setuptools'],},
    zip_safe=False,
    install_requires = ['py>=1.3.1'],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS :: MacOS X',
    'Topic :: Software Development :: Testing',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Utilities',
    'Programming Language :: Python',
    ],
)
