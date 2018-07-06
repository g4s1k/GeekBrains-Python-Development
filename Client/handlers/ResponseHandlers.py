import logging


deblog = logging.getLogger('deblogger')
errlog = logging.getLogger('errlogger')


class ResponseHandlers():

    def __init__(self):
        pass
    
    @classmethod
    def connect(cls, client):
        try:
            recieved_pack = client._inputbuf
            if recieved_pack.code == 200:
                message = recieved_pack.body['message']
                online_list = recieved_pack.body['online']
                client._online_list.update(online_list)
                client.onlineListRecieved.emit()
                return ('service', 'Server', message)
            else:
                return ('service', 'System', 'Server don\'t response.')
        except:
            errlog.exception('Error occured')

    @classmethod
    def message(cls, client):
        try:
            recieved_pack = client._inputbuf
            message = recieved_pack.body['message']
            if recieved_pack.code == 200:
                pass #тут будет маркер доставки
            elif recieved_pack.code == 300:
                return ('service', 'Server', message) #пользователь не найден
            else:
                sender = recieved_pack.body['sender']
                recip = recieved_pack.body['recipient']
                if recip == 2:
                    type = 'public'
                else:
                    type = 'private'
                return (type, sender, message)
        except:
            errlog.exception('Error occured')

    @classmethod
    def authoreg(cls, client):
        try:
            recieved_pack = client._inputbuf
            message = recieved_pack.body['message']
            if recieved_pack.code == 200:
                client._username = recieved_pack.body['username']
            elif recieved_pack.code == 100:
                user = recieved_pack.body['new_user']
                client._online_list.update(user)
                client.newUserOnline.emit(user)
            return ('service', 'Server', message)
        except:
            errlog.exception('Error occured')

    @classmethod
    def disconnect(cls, client):
        try:
            recieved_pack = client._inputbuf
            message = recieved_pack.body['message']
            user = recieved_pack.body['user']
            user_id = tuple(user.keys())[0]
            if client._username in user.values():
                client._connected = False
                client._exit = True
                client._username = None
                client._c_socket.close()
                client._c_socket = None
            else:
                client._online_list.pop(user_id)
                client.userDisconnected.emit(user)
                message = f'{user[user_id]} disconnected.'
            return ('service', 'Server', message)
        except:
            errlog.exception('Error occured')

