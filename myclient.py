import socket
import mycssettings as settings
import jimprotocol as jim
import datetime
from carnival import ClientStuffDealer as CSD
import logging
import logsettings
import carnival


deblog = logging.getLogger('deblogger')
errlog = logging.getLogger('errlogger')


class MyClient:
    def __init__(self):
        self._c_socket = socket.socket()
        self._buf = jim.JimPocket('client')
        self._exit = False
        self._dis = False

    @carnival.log
    def read_data(self):
        try:
            data = self._c_socket.recv(settings.BUF_SIZE)
            if data:
                self._buf.pack_it(data)
            self._buf.deserialise()
        except (ConnectionResetError, BrokenPipeError) as err:
            errlog.error(f'Connection error: {err}')
            print('Disconnected.')
        except:
            errlog.exception('Error occured')

    @carnival.log
    def enter_data(self):
        data = input('Data input: ')
        if data.lower().startswith('/'):
            self.command_packing(data)
        else:
            self.message_packing(data)

    @carnival.log
    @CSD.connect_response_handler
    @CSD.auth_response_handler
    def factory(self):
        try:
            recieved_pack = self._buf
            if self._dis or self._exit:
                if recieved_pack.code == 200:
                    print('Disconnected from the server.')
                else:
                    print('Disconnected, but server response didn\'t recieved.')
                if self._c_socket:
                    self._c_socket.close()
        except:
            errlog.exception('Error occured')

    @carnival.log
    @CSD.connect_com_adder
    @CSD.auth_com_adder
    def command_packing(self, data):
        if data == '/dis':
            self._dis = True
            self._buf.newpack(0, 'disconnect', {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                              {'command': data})
        elif data == '/exit':
            self._exit = True
            self._buf.newpack(0, 'disconnect', {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                              {'command': data})

    @carnival.log
    def message_packing(self, data):
        self._buf.newpack(0, 'message', {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}, {'message': data})

    @carnival.log
    def send_data(self):
        try:
            self._buf.serialise()
            data = self._buf.pack
            self._c_socket.send(data)
        except (ConnectionResetError, BrokenPipeError) as err:
            errlog.error(f'Connection error: {err}')
            print('Disconnected.')
        except:
            errlog.exception('Error occured')

    @carnival.log
    def start(self):
        try:
            self._exit = False
#            self._c_socket.connect((settings.SERV_HOST, settings.SERV_PORT))
#            print(f'Connected to {settings.SERV_HOST}:{settings.SERV_PORT}')
            while not self._exit:
                self.enter_data()
#                self._buf.show_pack()
                self.send_data()
                self.read_data()
                self.factory()
#                self._buf.show_pack()
            print('See you!')
        except KeyboardInterrupt:
            # Обрабатываем сочетание клавишь Ctrl+C
            pass
        except:
            errlog.exception('Error occured')

if __name__ == '__main__':
    client = MyClient()
    client.start()
