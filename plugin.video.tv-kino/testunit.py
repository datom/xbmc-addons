# http://docs.python.org/release/2.6.6/library/unittest.html
import unittest
import tv_kino


class test_tv_kino(unittest.TestCase):
    
    """
    test tv-kino model
    """
    
    tv_kino = None

    def setUp(self):
        """
        set up data used in the tests.
        setUp is called before each test function execution.
        """
        
        self.tv_kino = tv_kino.tv_kino()
        
        

    def test_getChannels(self):
        
        channels = self.tv_kino.getChannels()

        self.assertNotEqual(len(channels), 0)

        for channel in channels:
            self.assertNotEqual(channel, tv_kino.Channel)
            self.assertNotEqual(channel.name, "")
            self.assertNotEqual(channel.logo, "")
            self.assertNotEqual(channel.lang, "")
            


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test_tv_kino))
    return suite

if __name__ == '__main__':
    unittest.main()