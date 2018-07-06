from Net import mycssettings as settings
import datetime
import logging
import socket


deblog = logging.getLogger('deblogger')
errlog = logging.getLogger('errlogger')


class EventHandlers():

    def __init__(self):
        pass

    @classmethod
    def connect(cls, client):
        try:
            client._c_socket = socket.socket()
            client._c_socket.connect((settings.SERV_HOST, settings.SERV_PORT))
            client._connected = True
            client._outputbuf.newpack(0, 'connect', {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                   {})
            client.send_data()
        except:
            errlog.exception('Error occured')

    @classmethod
    def authorise(cls, login, password, client):
        try:
            client._outputbuf.newpack(0, 'authorise', {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                       {'login': login, 'password': password})
            client.send_data()
        except:
            errlog.exception('Error occured')

    @classmethod
    def registration(cls, name, login, password, client):
        try:
            client._outputbuf.newpack(0, 'registration', {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                       {'username': name, 'login': login, 'password': password})
            client.send_data()
        except:
            errlog.exception('Error occured')


    @classmethod
    def disconnect(cls, client):
        try:
            client._outputbuf.newpack(0, 'disconnect', {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                       {})
            client.send_data()
        except:
            errlog.exception('Error occured')

    @classmethod
    def send_message(cls, message, client, recipient):
        try:
            for id, name in client._online_list.items():
                if name == recipient:
                    recip_id = id
            client._outputbuf.newpack(0, 'message', {'time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")},
                                       {'message': message, 'recipient': recip_id})
            print(client._outputbuf.pack)
            client.send_data()
        except:
            errlog.exception('Error occured')
