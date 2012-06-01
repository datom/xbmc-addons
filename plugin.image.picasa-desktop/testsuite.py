# http://agiletesting.blogspot.com/2005/01/python-unit-testing-part-1-unittest.html
import os, unittest

suite = unittest.TestSuite()

if os.name == 'nt':
    import tests.win_default
    suite.addTest(tests.win_default.suite())
    
    import tests.win_network
    suite.addTest(tests.win_network.suite())
    
elif os.name == 'posix':
    import tests.unix_default
    suite.addTest(tests.unix_default.suite())
    
    import tests.unix_network
    suite.addTest(tests.unix_network.suite())


unittest.TextTestRunner(verbosity=2).run(suite)
