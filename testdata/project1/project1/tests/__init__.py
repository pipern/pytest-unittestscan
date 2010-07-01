import unittest

def suite():
    suite = unittest.TestLoader().loadTestsFromNames([
        'project1.tests.sampletest',
        ])

    return suite

