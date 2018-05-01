'''lets play!'''
import mycssettings as settings
import datetime
import logging


deblog = logging.getLogger('deblogger')
errlog = logging.getLogger('errlogger')

def log(func):
    def wrap(*args, **kwargs):
        func(*args, **kwargs)
        if __debug__:
            deblog.debug(f'args: {args}, kwargs: {kwargs}')
    return wrap


class ClientStuffDealer():

    def __init__(self):
        pass

    @classmethod
    def connect_com_adder(cls, command_packing_method):
        def new_logic(self, com):
            if com == '/connect':
                try:
                    self._c_socket.connect((settings.SERV_HOST, settings.SERV_PORT))
                    self._buf.newpack(0, 'connect', {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                  {'command': com})
                except:
                    errlog.exception('Error occured')
            else:
                command_packing_method(self, com)
        return new_logic

    @classmethod
    def auth_com_adder(cls, command_packing_method):
        def new_logic(self, com):
            if com == '/authorise':
                try:
                    name = input('Please enter the username: ')
                    passw = input('Please enter the password: ')
                    self._buf.newpack(0, 'authorise', {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                      {'name': name, 'passw': passw})
                except:
                    errlog.exception('Error occured')
            else:
                command_packing_method(self, com)
        return new_logic

    @classmethod
    def connect_response_handler(cls, factory):
        def new_shop(self):
            try:
                factory(self)
                recieved_pack = self._buf
                message = self._buf.pack['body']['message']
                if recieved_pack.action == 'connect':
                    if recieved_pack.code == 200:
                        print(message)
                    else:
                        print('Server don\'t response.')
            except:
                errlog.exception('Error occured')
        return new_shop

    @classmethod
    def auth_response_handler(cls, factory):
        def new_shop(self):
            try:
                factory(self)
                recieved_pack = self._buf
                message = self._buf.pack['body']['message']
                if recieved_pack.action == 'authorise':
                    if recieved_pack.code == 200:
                        print(message)
                    elif recieved_pack.code == 400:
                        print(f'{message} Please try again.')
                    else:
                        print('Server don\'t response.')
            except:
                errlog.exception('Error occured')
        return new_shop


class ServerStuffDealer():

    def __init__(self):
        pass

    @classmethod
    def dis_event_handler(cls, factory):
        def new_shop(self, pack, client, wlist):
            if pack.action == 'disconnect':
                try:
                    self._buf.newpack(200, pack.action, {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                      {'message': 'Done.'})
                    if client in wlist:
                        self.send_data(client)
                        client.close()
                    print(f'{self._connections_list[client]} disconnected.')
                    self._connections_list.pop(client)
                except:
                    errlog.exception('Error occured')
            else:
                factory(self, pack, client, wlist)
        return new_shop

    @classmethod
    def message_event_handler(cls, factory):
        def new_shop(self, pack, client, wlist):
            if pack.action == 'message':
                try:
                    message = self._buf.pack['body']['message']
                    print(f'{self._connections_list[client]}: {message}')
                    self._buf.newpack(200, pack.action, {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                      {'message': 'Message received'})
                    if client in wlist:
                        self.send_data(client)
                except:
                    errlog.exception('Error occured')
            else:
                factory(self, pack, client, wlist)

        return new_shop

    @classmethod
    def auth_event_handler(cls, factory):
        def new_shop(self, pack, client, wlist):
            if pack.action == 'authorise':
                try:
                    for title, data in pack.body:
                        if title == 'name':
                            name = data
                        elif title == 'passw':
                            passw = data
                    auth = False
                    users_list = open('users.txt', 'r')
                    for userpass in users_list:
                        if f'{name} {passw}' in userpass:
                            auth = True
                    if auth:
                        #here will be something else....soon;)
                        self._buf.newpack(200, pack.action, {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                          {'message': 'Done.'})
                        print(f'User {name} is authorised.')
                    else:
                        self._buf.newpack(400, pack.action, {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                          {'message': 'Invalid username password pair.'})
                        print(f'Authorisation request from {self._connections_list[client]} failed.')
                    if client in wlist:
                        self.send_data(client)
                    users_list.close()
                except:
                    errlog.exception('Error occured')
            else:
                factory(self, pack, client, wlist)
        return new_shop
