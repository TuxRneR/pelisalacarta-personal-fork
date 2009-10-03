# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pintadibujos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import megavideo
import servertools
import binascii
import xbmctools

CHANNELNAME = "pintadibujos"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[pintadibujos.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[pintadibujos.py] mainlist")
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Ultimas novedades" , "http://www.pintadibujos.com/novedadesf.html" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Clasicos Disney" , "http://www.pintadibujos.com/disneyf.html" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Peliculas Princesas" , "http://www.pintadibujos.com/princesasf.html" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Peliculas Superheroes" , "http://www.pintadibujos.com/superheroesf.html" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Peliculas series TV" , "http://www.pintadibujos.com/seriesf.html" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Peliculas Anime" , "http://www.pintadibujos.com/animef.html" , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def movielist(params,url,category):
	xbmc.output("[pintadibujos.py] mainlist")

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<td><a href="([^"]+)" target="_blank"><img SRC="([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = urlparse.urljoin(url,match[0])

		# URL
		scrapedurl = urlparse.urljoin(url,match[0])
		
		# Thumbnail
		scrapedthumbnail = urlparse.urljoin(url,match[1])
		
		# procesa el resto
		scrapeddescription = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# A�ade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "detail" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
	xbmc.output("[pintadibujos.py] detail")

	title = params.get("title")
	thumbnail = params.get("thumbnail")
	xbmc.output("[pintadibujos.py] title="+title)
	xbmc.output("[pintadibujos.py] thumbnail="+thumbnail)

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	for video in listavideos:
		xbmctools.addvideo( CHANNELNAME , "Megavideo - "+video[0] , video[1] , category , video[2] )
	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[pintadibujos.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	xbmc.output("[pintadibujos.py] thumbnail="+thumbnail)
	xbmc.output("[pintadibujos.py] server="+server)
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

#mainlist(None,"","mainlist")
#detail(None,"http://impresionante.tv/ponyo.html","play")
