import socket
import netsettings as settings
import collections as col
import jimprotocol as jim
from eventhandlers import EvHandlers
import select
import logging
import datastore as ds


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
        self._session = ds.Session()

    def accept_connection(self):
        try:
            c_socket, c_adr =  self._l_socket.accept()
            adr_id = ds.Adress.get_adr_id(self._session, c_adr)
            ds.Journal.write(self._session, 'Connected', adr_id)
            self._connections_list.update({c_socket: adr_id})
        except socket.timeout:
            pass
        except:
            errlog.exception('Error occured')

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
                EvHandlers.dis(self, client)
        except:
            errlog.exception('Error occured')

    def echo(sending_func):
        def wrap(self, client, pack):
            pack.show_pack()
            pack.set_code(200)
            sending_func(self, client, pack)
        return wrap

    def send_data(self, client):
        try:
            pack = self._buf
            pack.serialise()
            data = pack.pack
            if client in self.wlist:
                client.send(data)
        except (ConnectionResetError, BrokenPipeError) as err:
            errlog.error('Connection error')
            if client in self._connections_list:
                EvHandlers.dis(self, client)
        except:
            errlog.exception('Error occured')

    @EvHandlers.connect
    @EvHandlers.registration
    @EvHandlers.message
    @EvHandlers.authorisation
    @EvHandlers.disconnect
    def request_handler(self, pack, client):
        pass

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
                    self.rlist, self.wlist, self.xlist = select.select(clients, clients, [], 0)
                for client in clients_list:
                    if client in self.rlist:
                        self.read_data(client)
                    if self._requests_list:
                        current_req = self._requests_list.popleft()
                        self.request_handler(current_req, client)
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

    def stop(self):
        self._stop = True

    def restart(self):
        self.stop()
        self.start()

if __name__ == '__main__':
    echo = MyServer()
    echo.start()
