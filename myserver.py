import socket
import mycssettings as settings
import collections as col
import jimprotocol as jim
import datetime
from carnival import ServerStuffDealer as SSD
import select
import logging
import carnival


deblog = logging.getLogger('deblogger')
errlog = logging.getLogger('errlogger')


class MyServer():
    def __init__(self):
        self._l_socket = socket.socket()
        self._l_socket.bind((settings.SERV_HOST, settings.SERV_PORT))
        print(f'Initialising done \n adress {settings.SERV_HOST}:{settings.SERV_PORT}')
        self._connections_list = {}
        self._requests_list = col.deque()
        self._l_socket.settimeout(settings.TIMEOUT)
        self._buf = jim.JimPocket('server')
        self._stop = False

    @carnival.log
    def accept_connection(self):
        try:
            c_socket, c_addr =  self._l_socket.accept()
            self._connections_list.update({c_socket: c_addr})
            print(f'{c_addr} connected. \n Waiting for incoming data:')
        except socket.timeout:
            pass
        except:
            errlog.exception('Error occured')

    @carnival.log
    def read_data(self, client):
        try:
            data = client.recv(settings.BUF_SIZE)
            if data:
                self._buf.pack_it(data)
                self._buf.deserialise()
                self._requests_list.append(self._buf)
        except ConnectionResetError:
            errlog.error('Connection error')
            if client in self._connections_list:
                print(f'{self._connections_list[client]} disconnected.')
                self._connections_list.pop(client)
        except:
            errlog.exception('Error occured')

    def echo(sending_func):
        def wrap(self, client, pack):
            pack.show_pack()
            pack.set_code(200)
            sending_func(self, client, pack)
        return wrap

    @carnival.log
    def send_data(self, client):
        try:
            pack = self._buf
            pack.serialise()
            data = pack.pack
            client.send(data)
        except (ConnectionResetError, BrokenPipeError) as err:
            print(f'{self._connections_list[client]} disconnected.')
            self._connections_list.pop(client)
            errlog.error(f'Connection error: {err}')
        except:
            errlog.exception('Error occured')

    @carnival.log
    @SSD.dis_event_handler
    @SSD.auth_event_handler
    @SSD.message_event_handler
    def factory(self, pack, client, wlist):
        try:
            if pack.action == 'connect':
                self._buf.newpack(200, pack.action, {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                  {'message': 'Connection accepted.'})
                if client in wlist:
                    self.send_data(client)
        except:
            errlog.exception('Error occured')

    @carnival.log
    def start(self):
        try:
            self._stop = False
            self._l_socket.listen(settings.CONNECTIONS_COUNT)
            print(f'Server starting done. Max supported clients count is {settings.CONNECTIONS_COUNT}\n Waiting for clients')
            while not self._stop:
                self.accept_connection()
                clients_list = {}
                clients_list.update(self._connections_list)
                clients = clients_list.keys()
                if clients:
                    rlist, wlist, xlist = select.select(clients, clients, [], 0)
                for client in clients_list:
                    if client in rlist:
                        self.read_data(client)
                    if self._requests_list:
                        current_req = self._requests_list.popleft()
                        self.factory(current_req, client, wlist)
                        #self.send_data(client)
                #self.sentinel()
            print('Server stopped')
        except KeyboardInterrupt:
            pass
        except:
            errlog.exception('Error occured')

    # def look(self, pack):
    #     body = dict(pack.body)
    #     if '/stop' in tuple(body.values()):
    #         self.stop()

    @carnival.log
    def stop(self):
        self._stop = True


    @carnival.log
    def restart(self):
        self.stop()
        self.start()

if __name__ == '__main__':
    echo = MyServer()
    echo.start()
