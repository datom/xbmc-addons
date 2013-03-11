import sys
import xbmcgui
from addon import AddonHelper
from tv_kino import *


class tv_kinoAddon(AddonHelper):
	
	domain = "http://www.tv-kino.net"
	tv_kino = None
	
	def __init__(self):
		AddonHelper.__init__(self,'plugin.video.tv-kino')
		self.tv_kino = tv_kino()
		
		# what todo?
		try:
			if self.getParamString('channel_url', None):
				self.playChannel( channel_url = self.getParamString('channel_url', None) )
				
			else:
				self.listChannels()
		
		except Exception, e: # python 2.6 as
			xbmcgui.Dialog().ok('Error', e.__str__())
		
		return None


	def listChannels(self):
		""" get available channels """
		
		channels = self.tv_kino.getChannels()
		for channel in channels:
			
			#print "Channel: " + m[3]
			#print "Lang: " + m[1]
			#print "Link: " + self.domain + m[0]
			#print "Logo: " + m[2]
			
			liz = self.xbmcgui().ListItem(label = channel.name, thumbnailImage = channel.logo)
			liz.setInfo(type = "video", infoLabels = {
												#"title": m[3],
												#"duration": "8:10",
												#"tagline": "lauft gerade...",
												"language": channel.lang
			} )

			url = self.tv_kino.getStreamUrl( channel )

			self.xbmcplugin().addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False,totalItems=len(channels))
			
			#self.addDir(_name = m[3], _thumbnail = m[2], _total=len(m), channel_url = m[0] )
		
		self.endOfDirectory(succeeded=True,updateListing=False,cacheToDisc=True)
	
	

# main
tv_kinoAddon()
