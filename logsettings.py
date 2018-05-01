import logging
from logging import handlers


#Format settings
FORMAT = '%(asctime)s    %(modulename)s  --  %(levelname)s: %(message)s'
debformatter = logging.Formatter('%(asctime)s    %(modulename)s  --  %(levelname)s: %(funcName)s %(message)s')

#Basic config settings
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

#Logger objects creation
deblogger = logging.getLogger('deblogger')
errlogger = logging.getLogger('errlogger')


#Handlers creation
debclientfile = logging.FileHandler('debugclient.txt')
debservfile = logging.handlers.TimedRotatingFileHandler('debugclient.txt', when='midnight', interval=1, backupCount=7)
errfile = logging.FileHandler('errlog.txt')

#Handlers format settings
debclientfile.setFormatter(debformatter)
debservfile.setFormatter(debformatter)

#Adding handlers to logger objects
deblogger.addHandler(debclientfile)
deblogger.addHandler(debservfile)
errlogger.addHandler(errfile)

