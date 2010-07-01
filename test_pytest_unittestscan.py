"""
run "python setup.py develop" before running the contained test
"""
import py

pytest_plugins = "pytester", "setuptools"
