﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videobb
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os,re

try:
    from core import scrapertools
    from core import logger
    from core import config
except:
    from Code.core import scrapertools
    from Code.core import logger
    from Code.core import config

_VALID_URL = r'^((?:http://)?(?:\w+\.)?videobb\.com/(?:(?:e/)|(?:(?:video/)?))?)?([0-9A-Za-z_-]+)(?(1).+)?$'
COOKIEFILE = os.path.join(config.get_data_path() , "cookies.lwp")

# Obtiene la URL que hay detrás de un enlace a linkbucks
def geturl(url):

    logger.info("[videobb.py] url="+url)
    # El formato de la URL de la página es
    # http://videobb.com/video/zFFw8n8w1r1s
    # El formato de la URL del vídeo es
    # http://s.videobb.com/s2?v=zFFw8n8w1r1s&r=1&t=1294503726&u=&c=ad60cbaec0af97d5d911d5a236841b42&start=0
    url = Extract_id(url)
    if url:
        devuelve = "http://s.videobb.com/s2?v=" + url
    else: 
        return ""
    import random
    devuelve = "%s&r=1&t=%d&u=&c=12&start=0" % (devuelve,random.randint(1000000000,9999999999))

    logger.info("[videobb.py] url="+devuelve)
    
    return devuelve

def Extract_id(url):
	# Extract video id from URL
	mobj = re.match(_VALID_URL, url)
	if mobj is None:
		print 'ERROR: URL invalida: %s' % url
		
		return ""
	id = mobj.group(2)
	return id