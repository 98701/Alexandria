import logging

var = 1
loglevel = logging.DEBUG if var == 1 else logging.WARNING

logging.basicConfig(#filename='loggg.log', filemode='a', 
    format='%(asctime)s %(message)s', level=loglevel)
logger = logging.getLogger()

logger.debug('Hi')

