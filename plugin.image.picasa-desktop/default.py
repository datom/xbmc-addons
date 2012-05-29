import os, re, glob
import xbmcgui
from addon import AddonHelper
from picasa import PicasaKit


__plugin__ =	'picasa-desktop'
__author__ = 'datom'
__url__ = ''
__date__ = '02-04-2012'
__version__ = '0.1.0'


class picasaDesktop(AddonHelper):
	_picasa = None
	
	def __init__(self):
		AddonHelper.__init__(self,'plugin.image.picasa-desktop')
		
		if self.getSettingInt('db_location') == 0:
			# default local picasa db
			if os.name == 'nt':
				db_path = "file://" + os.path.join(os.getenv('USERPROFILE'), 'appdata', 'Local', 'Google', 'Picasa2Albums')
			elif os.name == 'posix':
				db_path = "file://" + os.path.join(os.getenv('HOME'), '.google', 'picasa', '3.0', 'drive_c', 'Documents and Settings', os.getenv('USER'), 'Local Settings', 'Application Data', 'Google', 'Picasa2Albums')
				
			protocol = PicasaKit().createProtocolFromString(db_path)
			
			m = re.match('\w+://(.*)', db_path)
			db_search = m.group(1)
			
		elif self.getSettingInt('db_location') == 1:
			# local folder
			db_path = "file://" + self.getSetting('db_path_local')
			protocol = PicasaKit().createProtocolFromString(db_path)
			
			m = re.match('\w+://(.*)', db_path)
			db_search = m.group(1)
			
		else:
			# network
			db_path = self.getSetting('db_path_network')
			m = re.match('\w+://(.+?)/', db_path)
			protocol = PicasaKit().createProtocolFromString(db_path)
			protocol.connect(username = self.getSetting('db_path_network_user'), password = self.getSetting('db_path_network_pass'), ip = m.group(1))
			
			m = re.match('\w+://(.*)', db_path)
			db_search = '/' + m.group(1)
		
		
		# search for database files...
		print "search database..."
		location = PicasaKit().createLocation(protocol)
		if location.search_database(db_search) == False:
			print db_search
			xbmcgui.Dialog().ok('Picasa Desktop', 'Database not found at\n[%s]' % db_search)
			return None
		
		# init
		print "use path: " + location.cwd()
		self._picasa = PicasaKit().createDatabase(location)
		
		
		
		# what todo?
		try:
			if self.getParamString('album', None):
				self.listImages( album_id = self.getParamString('album', None) )
				
			else:
				self.listAlbum()
		
		except Exception, e: # python 2.6 as
			xbmcgui.Dialog().ok('Picasa Error', e.__str__())
		
		return None


	def listAlbum(self):
		""" show picasa albums """
		albumlist = self._picasa.albums()
		for item in albumlist:
			album = self._picasa.album(item.id())
			images = album.files()
			self.addDir(_name = album.name(), _thumbnail=images[0], _total=len(albumlist), album = album.id() )
		
		self.endOfDirectory(succeeded=True,updateListing=False,cacheToDisc=True)
	
	
	def listImages(self, album_id):
		""" show images from an album """
		album = self._picasa.album(album_id)
		for image in album.files():
			url = image
			# FIXME
			name = re.sub(r'.*%s(.+)\.\w{3,4}' % (re.escape(os.sep)), r'\1', image)
			self.addLink(name=name, url=image, thumbnail=image, total=len(album.files()),contextMenu=None)
		
		self.endOfDirectory(succeeded=True,updateListing=False,cacheToDisc=True)



# main
picasaDesktop()