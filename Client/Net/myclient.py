from . import mycssettings as settings
from . import jimprotocol as jim
import logging
from handlers.HandlersList import HL
from queue import Queue
from PyQt5.QtCore import QObject, pyqtSignal

deblog = logging.getLogger('deblogger')
errlog = logging.getLogger('errlogger')


class MyClient(QObject):

    incomingMessage = pyqtSignal(Queue)
    onlineListRecieved = pyqtSignal()
    newUserOnline = pyqtSignal(dict)
    userDisconnected = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._c_socket = None
        self._inputbuf = jim.JimPocket('client')
        self._outputbuf = jim.JimPocket('client')
        self._exit = False
        self._connected = False
        self._incoming_list = Queue()
        self._username = None
        self._online_list = {2: 'All users'}

    def read_data(self):
        try:
            data = self._c_socket.recv(settings.BUF_SIZE)
            if data:
                self._inputbuf.pack_it(data)
                self._inputbuf.deserialise()
                return True
        except (ConnectionResetError, BrokenPipeError) as err:
            errlog.error(f'Connection error: {err}')
            print('Disconnected.')
        except:
            errlog.exception('Error occured')

    def send_data(self):
        try:
            self._outputbuf.serialise()
            data = self._outputbuf.pack
            self._c_socket.send(data)
        except (ConnectionResetError, BrokenPipeError) as err:
            errlog.error(f'Connection error: {err}')
            print('Disconnected.')
        except:
            errlog.exception('Error occured')

    def listen(self):
        try:
            self._exit = False
            while not self._exit:
                if (self._connected and self.read_data()):
                    response_handler = HL[self._inputbuf.action]
                    self._incoming_list.put(response_handler(self))
                    self.incomingMessage.emit(self._incoming_list)
        except KeyboardInterrupt:
            pass
        except:
            errlog.exception('Error occured')
