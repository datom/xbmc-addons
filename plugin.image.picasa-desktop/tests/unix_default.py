# http://docs.python.org/release/2.6.6/library/unittest.html
import unittest, os, re
from picasa import PicasaKit


class testPicasaLinuxDefault(unittest.TestCase):
    
    """
    A test class for the PicasaKit module.
    System:
    Ubuntu 10.10
    Picasa 3
    Default Database
    """

    def setUp(self):
        """
        set up data used in the tests.
        setUp is called before each test function execution.
        """
        
        
        db_path = "file://" + os.path.join(os.getenv('HOME'), '.google', 'picasa', '3.0', 'drive_c', 'Documents and Settings', os.getenv('USER'), 'Local Settings', 'Application Data', 'Google', 'Picasa2Albums')
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
        self.assertNotEqual( self.picasa.album('21f2c0b53018628cbea72ad28503a41d'), Album)




def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testPicasaLinuxDefault))
    return suite

if __name__ == '__main__':
    unittest.main()