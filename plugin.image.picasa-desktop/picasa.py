import os, re, glob
import xml.dom.minidom
import exceptions



# GoF: Abstract Factory
class PicasaKit:
	def createProtocolFromString(self, path):
		
		# check protocol
		m = re.match('(\w+)://.*', path)
		if m.group(1) == 'file':
			return ProtocolLocal()
			
		elif m.group(1) == 'smb':
			return ProtocolSMB()
		
		else:
			raise IOError('unkown location string')

	def createLocation(self, protocol):
		return PicasaLocation(protocol)
	
	def createDatabase(self, location):
		return PicasaDatabase(location)
	

class Album(object):
	_files = list()
	
	def set_id(self, id):
		self._id = id
	
	def id(self):
		return self._id
	
	def set_name(self, name):
		self._name = name
		
	def name(self):
		return self._name
	
	def files(self):
		return self._files



class ILocation(object):
	
	""" Interface for different locations like local host or network """
	
	def listDir(self, path):
		raise IOError('function not implemented')
	
	def readFile(self, filename):
		raise IOError('function not implemented')

	def listFiles(self, path):
		raise IOError('function not implemented')
	
	def generate_path(self, *p):
		raise IOError('function not implemented')


class ProtocolLocal(ILocation):
	
	def listFile(self, path):
		list = []
		for infile in os.listdir(path):
			list.append(infile)
			
		return list
	
	def listDir(self, path):
		list = []
		for dir in os.listdir(path):
			list.append(dir)

		return list
	
	def readFile(self, filename):
		f = open(filename)
		buffer = ""
		try:
			for line in f:
				buffer +=line
		finally:
			f.close()

		return buffer
	
	def generate_path(self, a, *p):
		return os.path.join(a, *p);


class ProtocolSMB(ILocation):
	
	"""
	Doku: http://packages.python.org/pysmb/api/smb_SMBConnection.html?highlight=listpath#smb.SMBConnection.SMBConnection.listPath
	"""
	
	_conn = None
	
	def __del__(self):
		self._conn.close()
		
	
	def connect(self, username, password, ip):
		""" remote connect smb """
		from smb.SMBConnection import SMBConnection
		
		self._conn = SMBConnection(username, password, my_name = "", remote_name = "", domain='', use_ntlm_v2=True)
		return self._conn.connect(ip = ip, timeout = 5)
		

	def listDir(self, path):
		m = re.match('/.+?/(.+?)/(.+)', path)
		share = m.group(1)
		folder = m.group(2)
		
		list = []
		for item in self._conn.listPath(share, folder):
			if item.isDirectory and item.filename[0] != '.':
				list.append( item.filename )

		return list
	
	def listFile(self, path):
		m = re.match('/.+?/(.+?)/(.+)', path)
		share = m.group(1)
		folder = m.group(2)
		#filter = m.group(3)
		
		list = []
		for item in self._conn.listPath(share, folder):
			if item.isDirectory == False:
				list.append( item.filename )

		return list
		
	
	def readFile(self, filename):
		m = re.match('/.+?/(.*?)/(.*)', filename)
		share = m.group(1)
		folder = m.group(2)
		
		import tempfile
		
		tmpfile = tempfile.TemporaryFile()
		self._conn.retrieveFile(share, folder, tmpfile)
		
		tmpfile.seek(0)
		buffer = ""
		try:
			for line in tmpfile:
				buffer +=line
		finally:
			tmpfile.close()

		return buffer

	def generate_path(self, a, *p):
		chdir = a
		for path in p:
			chdir = chdir + '/' + path
			
		return chdir



class PicasaLocation(object):
	
	_protocol = None
	_working_directory = None
	
	def __init__(self, protocol):
		self._protocol = protocol
	
	def search_database(self, path):
		""" search picasa database backup files """
		
		try:
			# picasa <= 3.8
			for dir in self._protocol.listDir(path):
				if re.search('^[\w\d]{32}$', dir):
					self._working_directory = self._protocol.generate_path(path, dir)
					return True
			
			# picasa 3.9
			# search for the latest backup
			import time, locale
			
			locale.setlocale(locale.LC_TIME, '')
			newest = time.strptime('1900', '%Y')
			use_dir = None
			
			for dir in self._protocol.listDir(self._protocol.generate_path(path, 'backup')):
				check = time.strptime(dir,'%A, %d. %B %Y')
				if check > newest:
					newest = check
					use_dir = dir
			
			self._working_directory = self._protocol.generate_path(path, 'backup', use_dir)
			#locale.resetlocale()
			return True
			
		except Exception, e:
			pass
			
		return False
	
	def listFiles(self):
		return self._protocol.listFile(self._working_directory)
	
	def readFile(self, file):
		return self._protocol.readFile(self._protocol.generate_path(self._working_directory, file))
	
	def cwd(self):
		return self._working_directory


class PicasaDatabase(object):
	
	_location = None
	
	def __init__(self, location):
		self._location = location


	def _getText(self, nodelist):
		rc = []
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE:
				rc.append(node.data)
		return ''.join(rc)



	def albums(self):
		""" list all available albums in picasa """
		
		list = []
		for file in self._location.listFiles():
			if re.search(r'.*(.{32})\.pal', file):
				id = re.sub(r'.*(.{32})\.pal' , r'\1', file)
				album = Album()
				album.set_id( id )
				list.append( album )
		
		return list


	def album(self, id):
		""" read album metadata and images """
		
		buffer = self._location.readFile(id + '.pal')
		album = Album()
		album._files = []
		album.set_id(id)
		
		""" extract data """
		dom = xml.dom.minidom.parseString(buffer)
		metainfo = { 'property': dict(), 'files': list() }
		
		for property in dom.getElementsByTagName("property"):
			metainfo['property'].update( {property.getAttribute("name"): property.getAttribute("value")} )
		
		album.set_name( metainfo['property']['name'] )
		for filenode in dom.getElementsByTagName("filename"):
			file = self._getText(filenode.childNodes)
			
			""" FIXME os related! """
			file = re.sub(r'\[([A-Z])\]{1}',r'\1:\\',file)										# replace drive letter
			file = re.sub(r'\$UNC(.*)',r'\\\1',file)											# network shortcut
			
			#file = re.sub(r'\$Desktop(.*)',os.getenv('USERPROFILE') + r'\Desktop\1',file)		# desktop shortcut
			
			""" FIXME UNIX """
			#<filename>$My Pictures\ > ~/Pictures/
			#//10.0.0.8/tom.....
			
			album._files.append(file)
		
		return album
