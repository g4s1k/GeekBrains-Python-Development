#import netsettings as settings
import datetime
import logging
import datastore as ds


deblog = logging.getLogger('deblogger')
errlog = logging.getLogger('errlogger')


class EvHandlers():

    def __init__(self):
        pass
    
    @classmethod
    def connect(cls, request_handler):
        def new_handler(self, pack, client):
            if pack.action == 'connect':
                try:
                    message = 'Connection accepted.'
                    online_list = {}
                    for client, info in self._connections_list.items():
                        if not isinstance(info, int):
                            user = info[1]
                            online_list.update({user.Id: user.Username})
                    self._buf.newpack(200, pack.action, {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                      {'message': message, 'online': online_list})
                    self.send_data(client)
                except:
                    errlog.exception('Error occured')
            else:
                request_handler(self, pack, client)
        return new_handler

    @classmethod
    def disconnect(cls, request_handler):
        def new_handler(self, pack, client):
            if pack.action == 'disconnect':
                try:
                    adr_id = self._connections_list[client][0]
                    user = self._connections_list[client][1]
                    ds.Journal.write(self._session, 'Disconnected', adr_id, user.Id)
                    self._buf.newpack(200, pack.action, {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                      {'message': 'Disconnected', 'user': {user.Id: user.Username}})
                    for socket, info in self._connections_list.items():
                        if not isinstance(info, int):
                            self.send_data(socket)
                    client.close()
                    print(f'{self._connections_list[client]} disconnected.')
                    self._connections_list.pop(client)
                except:
                    errlog.exception('Error occured')
            else:
                request_handler(self, pack, client)
        return new_handler

    @classmethod
    def message(cls, request_handler):
        def new_handler(self, pack, client):
            if pack.action == 'message':
                try:
                    action = pack.action
                    text = self._buf.body['message']
                    recip_id = self._buf.body['recipient']
                    sender = self._connections_list[client][1]
                    sender_adr_id = self._connections_list[client][0]
                    self._buf.body.update({'sender': sender.Username})
                    recip = self._session.query(ds.User).filter(ds.User.Id == recip_id).all()
                    # +Заготовочка под досылку сообщений пользователям не в сети
                    if recip:
                        recip = recip[0]
                        recip.Online = False
                        code = 200
                        info = 'Message was delivered'
                        for num, user in enumerate(self._connections_list.values()):
                            if (isinstance(user, tuple) and user[1].Id == recip.Id):
                                recip.Online = True
                                recip.socket = tuple(self._connections_list.keys())[num]
                                recip_adr_id = user[0]
                        if recip.Online:
                            self.send_data(recip.socket)
                        elif recip.Username == 'All users':
                            recip_adr_id = None
                            for socket in tuple(self._connections_list.keys()):
                                if socket != client:
                                    self.send_data(socket)
                        else:
                            recip_adr_id = self._session.query(ds.Adress).filter(ds.Adress.Adress == 'Offline').one().Id
                            info = 'User offline'
                        message = ds.Message.add_message(self._session, recip.Id, recip_adr_id, text)
                        ds.Journal.write(self._session, 'Message', sender_adr_id, sender.Id, message.Id)
                    else:
                        code = 300
                        info = 'User not found'
                        deblog.warning(f'Message with invalid recipient Id: {recip_id} was recieved from {sender.Username}')
                    self._buf.newpack(code, action, {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                          {'message': info})
                    self.send_data(client)
                except:
                    errlog.exception('Error occured')
            else:
                request_handler(self, pack, client)

        return new_handler

    @classmethod
    def authorisation(cls, request_handler):
        def new_handler(self, pack, client):
            if pack.action == 'authorise':
                try:
                    action = pack.action
                    for title, data in pack.body.items():
                        if title == 'login':
                            login = data
                        elif title == 'password':
                            passw = data
                    user = ds.User.authorise(self._session, login, passw)
                    adr_id = self._connections_list[client]
                    clients = []
                    if (user and ((adr_id, user) not in tuple(self._connections_list.values()))):
                        for client, info in self._connections_list.items():
                            if not isinstance(info, int):
                                clients.append(client)
                        ds.Journal.write(self._session, 'Authorised', adr_id, user.Id)
                        self._connections_list.update({client: (adr_id, user)})
                        self._buf.newpack(200, action, {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                          {'username': user.Username, 'message': f'Welcome back, {user.Username}!'})
                        print(f'User {user.Username} is authorised.')
                    elif ((adr_id, user) in tuple(self._connections_list.values())):
                        self._buf.newpack(400, action,
                                          {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                          {'message': f'Name {user.Username} already in use.'})
                    else:
                        deblog.info(f'Authorisation request failed from {self._connections_list[client]} with login: {login}')
                        self._buf.newpack(400, action, {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                          {'message': 'Invalid username password pair.'})
                    self.send_data(client)
                    if clients:
                        self._buf.newpack(100, action, {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                          {'new_user': {user.Id: user.Username}, 'message': f'{user.Username} connected.'})
                        for client in clients:
                            self.send_data(client)
                except:
                    errlog.exception('Error occured')
            else:
                request_handler(self, pack, client)
        return new_handler

    @classmethod
    def registration(cls, request_handler):
        def new_handler(self, pack, client):
            if pack.action == 'registration':
                try:
                    action = pack.action
                    for title, data in pack.body.items():
                        if title == 'username':
                            username = data
                        elif title == 'login':
                            login = data
                        elif title == 'password':
                            passw = data
                    user = ds.User.registration(self._session, username, login, passw)
                    adr_id = self._connections_list[client]
                    clients = []
                    if user:
                        for client, info in self._connections_list.items():
                            if not isinstance(info, int):
                                clients.append(client)
                        ds.Journal.write(self._session, 'Registered', adr_id, user.Id)
                        self._connections_list.update({client: (adr_id, user)})
                        self._buf.newpack(200, action, {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                          {'username': user.Username, 'message': f'Glad to see you, {user.Username}!'})
                        print(f'User {user.Username} is registered.')
                    else:
                        deblog.info(f'Registration request failed from {self._connections_list[client]} with name: {username}, login: {login}')
                        self._buf.newpack(400, action, {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                          {'message': 'Username or login already in use.'})
                    self.send_data(client)
                    if clients:
                        self._buf.newpack(100, action,
                                          {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                          {'new_user': {user.Id: user.Username}, 'message': f'{user.Username} connected.'})
                        for client in clients:
                            self.send_data(client)
                except:
                    errlog.exception('Error occured')
            else:
                request_handler(self, pack, client)
        return new_handler

    @classmethod
    def dis(cls, ServerObj, client):
        try:
            adr_id = ServerObj._connections_list[client][0]
            user = ServerObj._connections_list[client][1]
            ServerObj._connections_list.pop(client)
            client.close()
            ds.Journal.write(ServerObj._session, 'Disconnected', adr_id, user.Id)
            ServerObj._buf.newpack(200, 'disconnect', {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                               {'message': 'Disconnected', 'user': {user.Id: user.Username}})
            for socket, info in ServerObj._connections_list.items():
                if not isinstance(info, int):
                    ServerObj.send_data(socket)
            print(f'{ServerObj._connections_list[client]} disconnected.')
        except:
            errlog.exception('Error occured')
