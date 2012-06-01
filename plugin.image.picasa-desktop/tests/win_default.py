# http://docs.python.org/release/2.6.6/library/unittest.html
import unittest, os, re
from picasa import PicasaKit


class testPicasaWinDefault(unittest.TestCase):
    
    """
    A test class for the PicasaKit module.
    System:
    Windows 7
    Picasa 3
    Default Database
    """

    def setUp(self):
        """
        set up data used in the tests.
        setUp is called before each test function execution.
        """
        
        
        db_path = "file://" + os.path.join(os.getenv('USERPROFILE'), 'appdata', 'Local', 'Google', 'Picasa2Albums')
        protocol = PicasaKit().createProtocolFromString(db_path)
        location = PicasaKit().createLocation(protocol)
        
        # search for dbid...
        m = re.match('\w+://(.*)', db_path)
        location.search_database(m.group(1))
        
        # init
        self.picasa = PicasaKit().createDatabase(location)
        
        

    def test_ListAlbums(self):
        # 
        self.assertNotEqual( len(self.picasa.albums()), 0 )


    def test_ReadAlbum(self):
        # 
        from picasa import Album
        self.assertNotEqual( self.picasa.album('28e8b0464bcdd4b193b12b0c7301595a'), Album)




def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testPicasaWinDefault))
    return suite

if __name__ == '__main__':
    unittest.main()