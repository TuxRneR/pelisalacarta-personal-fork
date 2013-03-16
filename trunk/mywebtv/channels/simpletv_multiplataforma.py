# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal SimpleTV
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import sys
from core import scrapertools
from core import config
from core import logger
from core.item import Item

DEBUG = True
CHANNELNAME = "simpletv"

# Prioridad al cargar listas. 1=Archivo local, 0=URL's de internet y si no funcionan archivo local
simpletv_pri_local = 0

simpletv_urls = [
    'http://playlist.iptvonline.cu.cc/',
    'http://juanin.co.nf/mokolist.m3u'
]

# Archivo local
simpletv_local = os.path.join( config.get_runtime_path() , "streams" , "simpletv.m3u" )

def isGeneric():
    return True

def mainlist(item):
    logger.info("[simpletv.py] mainlist")

    lista_correcta = False
    if simpletv_pri_local == 0:
        # Descargar las distintas páginas que tienen las listas hasta que una sea válida
        for page_url in simpletv_urls:
            if lista_correcta: 
                print "Lista simpletv detectada"
                break

            print "Probando url: %s" % page_url
            data = scrapertools.cachePage(page_url)
        
            # Revisar si es un formulario para descargar la lista
            patron = '<form .*?method="post" action="(.*?)">.*?submit name="(.*?)" value="(.*?)"'
            matches = re.compile(patron,re.DOTALL).findall(data)
            if len(matches)==0:
                # Revisar si es una lista
                if re.search("#EXTINF:-1", data): lista_correcta = True
            else:
                if DEBUG: print "Formulario detectado"
                for match in matches:
                    page_url = "%s%s" % (page_url, str(match[0]))
                    page_post = "%s=%s" % (str(match[1]), str(match[2]))
                    if DEBUG: print "page_url: %s\npage_post: %s" % (page_url, page_post)
                    data = scrapertools.cachePage( page_url, post=page_post )
                    # Revisar si es una lista
                    if re.search("#EXTINF:-1", data): lista_correcta = True

    # Si no ha encontrado ninguna lista, leemos el archivo local
    # y si la ha encontrado la guardamos en el archivo local
    if not lista_correcta:
        import os.path
        if os.path.exists(simpletv_local):
            print "Leyendo archivo local de simpletv"
            f = open(simpletv_local)
            data = f.read()
            f.close()
        else:
            print "ERROR: No existe archivo local de simpletv"
            return []
    else:
        print "Guardando archivo local de simpletv"
        f = open(simpletv_local,"w")
        f.write(data)
        f.flush()
        f.close()
        
    # Busca el bloque con los canales
    itemlist = []
    patron = '#EXTINF:-1 \$ExtFilter="(.*?)",(.*?)(?:\n|\r|\r\n?)(.*?)(?:\n|\r|\r\n?)'
    matches = re.compile(patron,re.DOTALL|re.MULTILINE).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        if DEBUG: print "match: %s-%s-%s" % (match[0], match[1], match[2])
        if "Canales +18" in match[1]: continue
        if "RADIOS" in match[1]: continue
        if "Radios" in match[1]: continue
        if "RADIOS" in match[0]: continue
        if "Radios" in match[0]: continue
        scrapedtitle = match[0].upper() + ' - ' + match[1].upper()
        if match[2].startswith(("rtmp://", "rtmpt://", "rtmpe://", "rtmpte://", "rtmps://")):
            scrapedurl = match[2].replace("rtmp://$OPT:rtmp-raw=","").replace("live=1", "live=true").replace("--live","live=true")
            if not re.search(" timeout=", match[2]):
                scrapedurl = "%s%s" % (scrapedurl, " timeout=300")
        else:
            scrapedurl = match[2]
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle, url=scrapedurl, action="play", extra="rtmp", folder=True) )

    return itemlist

def play(item):
    logger.info("[simpletv.py] play")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="play", server="directo", title=item.title, url=item.url, thumbnail="", plot="", folder=False) )

    return itemlist