"""
py.test plugin to find unittest cases using the same method that
setuptools/setup.py uses.


Copyright 2010 (c) Logica

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
    
    Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.
    
    Neither the name of Logica nor the names of its contributors may
    be used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import py
import unittest

import sys
import ConfigParser

def pytest_ignore_collect(path, config):
    """Avoid py.test searching in build/ if setup.py exists. This
    stops it finding all the pyc files, which it considers to be in
    the wrong place.
    """
    if path.basename == "build":
        if path.dirpath("setup.py").check():
            return True

def pytest_collect_directory(path, parent):
    # ideally, we would find these by reading setup.py file
    # then looking at dependancies, and reading their setup.py
    # files for the test_suites value
    setupcfg = path.join("setup.cfg")
    if setupcfg.check():
        config = ConfigParser.ConfigParser()
        config.readfp(setupcfg.open())
        if config.has_section("pytest_unittest"):
            spec_list = config.get("pytest_unittest","scan").split()
            return UnitTestScan(setupcfg, parent, spec_list)

class UnitTestScan(py.test.collect.File):
    def __init__(self, name, parent, spec_list):
        super(UnitTestScan, self).__init__(name, parent)
        self.spec_list = spec_list
        
    def collect(self):
        for spec in self.spec_list:
            if ":" in spec:
                modname, funcname = spec.split(":")
                mod = __import__(modname, None, None, ['doc']) 
                func = getattr(mod, funcname)
                suites = func()
            else:
                mod = __import__(spec, None, None, ['doc'])
                from setuptools.command.test import ScanningLoader
                scanningLoader = ScanningLoader()
                suites = scanningLoader.loadTestsFromModule(mod)
            for item in suites:
                if isinstance(item, unittest.TestSuite):
                    yield UnitTestSuite("", parent=self, suite=item)

class UnitTestSuite(py.test.collect.Collector):
    def __init__(self, name, parent, suite):
        super(UnitTestSuite, self).__init__(name, parent)
        self.suite = suite

    def collect(self):
        for item in self.suite:
            if isinstance(item, unittest.TestSuite):
                yield UnitTestSuite("", parent=self, suite=item)
            elif isinstance(item, unittest.TestCase):
                yield UnitTestCase(item.id(), parent=self, case=item)

class UnitTestCase(py.test.collect.Collector):
    def __init__(self, name, parent, case):
        super(UnitTestCase, self).__init__(name, parent)
        self.obj = case
        # try discover the filesystem path for our test case 
        # so that py.test does nicer reporting 
        module = case.__module__
        mod = __import__(module, None, None, ['__doc'])
        fn = mod.__file__.rstrip("co")
        self.fspath = py.path.local(fn)
        
    def collect(self):
        plugin = self.config.pluginmanager.getplugin("unittest")
        return [plugin.UnitTestFunction(self.obj._testMethodName,
                                        parent=self)]

