# http://docs.python.org/release/2.6.6/library/unittest.html
import unittest, os, re
from picasa import PicasaKit


class testPicasaUnixNetwork(unittest.TestCase):
    
    """
    A test class for the PicasaKit module.
    System:
    Windows 7
    Picasa 3
    Network Database
    """

    def setUp(self):
        """
        set up data used in the tests.
        setUp is called before each test function execution.
        """
        
        
        db_path = "smb://10.0.0.11/tom/picasa/Local Settings/Application Data/Google/Picasa2Albums"
        protocol = PicasaKit().createProtocolFromString(db_path)
        protocol.connect(username = "Thomas Ballmann", password = "", ip = "10.0.0.11")
        location = PicasaKit().createLocation(protocol)
        
        # search for dbid...
        m = re.match('\w+://(.+)', db_path)
        location.search_database('/' + m.group(1))
        
        # init
        self.picasa = PicasaKit().createDatabase(location)
        
        

    def test_ListAlbums(self):
        #
        self.assertNotEqual( len(self.picasa.albums()), 0 )


    def test_ReadAlbum(self):
        #
        from picasa import Album
        self.assertNotEqual( self.picasa.album('84de3f2a5eb450e1aad57eaa7da06623'), Album)




def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testPicasaUnixNetwork))
    return suite

if __name__ == '__main__':
    unittest.main()