'''
Created on 14.06.2012

@author: Thomas Ballmann
'''

import urllib2, re

class tv_kino(object):
    '''
    classdocs
    '''
    
    domain = "http://www.tv-kino.net"


    def __init__(self):
        '''
        Constructor
        '''
        
        
    def getChannels(self):
        '''
        get available channels
        '''
        
        req = urllib2.Request(self.domain)
        response = urllib2.urlopen(req)
        content = response.read()
        response.close()
        
        match = re.compile('portfolio-thumbnail">.*?href="(.+?)".*?flags/(.+?).png".*?src="(.+?)".*?<h3>.*?>(.+?)</a>', re.DOTALL).findall(content)
        
        channels = []
        for m in match:
            #print "Channel: " + m[3]
            #print "Lang: " + m[1]
            #print "Link: " + self.domain + m[0]
            #print "Logo: " + m[2]
            #print "#########"
            
            channel = Channel()
            channel.lang = m[1]
            channel.logo = m[2]
            channel.name = m[3]
            #channel.link = m[0]
            
            channels.append(channel)
        
        
        match = re.compile('nownext_title">(.+?)<.*?background-size: (\d+)px.*?>(.+?)\((.+?)\)', re.DOTALL).findall(content)
        for m in match:
            #print "Now: " + m[0]
            #print "Progress: " + m[1] # str(int((100 / 210) * int(m[1]))) + "%", float(100 / 210), int(m[1]) # max = 210
            #print "Time: " + m[2]
            #print "Duration: " + m[3]
            #print "#########"
            pass
        
        return channels


    def getStream(self, channel):
        """
        read stream metadata
        """
        
        req = urllib2.Request(self.domain + channel.url)
        response = urllib2.urlopen(req)
        content = response.read()
        response.close()
        
        match = re.compile('"flashvars" value="(.+?)"', re.DOTALL).search(content)
        params = urllib2.unquote(match.group(1))
        
        print params
        print channel.getStream()
        
        # rtmp://live.tv-kino.net/stream playpath=ard swfUrl=http://stream.tv-kino.net/player.swf live=true
        



class Channel(object):
    
    name = ""
    lang = ""
    logo = ""
    


if __name__ == '__main__':
    tv_kino = tv_kino()
    channels = tv_kino.getChannels()
    
