import pytest
import mycssettings as settings
import socket
import jimprotocol


@pytest.fixture
def jimbeam(monkeypatch):

    class JimBeamBottle():

        def __init__(self, pocket_type):
            self.pocket_type = pocket_type.lower()
            if pocket_type == 'client':
                print('JimPocket object was initialised with "client" pocket type')
            elif pocket_type == 'server':
                print('JimPocket object was initialised with "server" pocket type')
            else:
                print('JimPocket object was initialised with incorrect pocket type!')
                self.pocket_type = 'incorrect'

    monkeypatch.setattr(jimprotocol, 'JimPocket', JimBeamBottle)


@pytest.fixture(autouse = True)
def mocksocketinterface(monkeypatch):

    class SocketMock():

        def __init__(self):
            print('Socket object was initialised.')
            self.type = 'socket object'

        def recv(self, arg):
            print(f'function recv was called with {arg} buf size')
            pack = jimprotocol.JimPocket('server')
            pack.newpack('zero', 'test', {'what time is it': '00.00'}, {'message': 'hey, dude!'})
            return pack.serialise()

        def bind(self, *args):
            print(f'function bind was called with {args} (host, port)')

        def connect(self, *args):
            print(f'function connect was called with {args} (host, port)')

        def accept(self):
            print(f'function accept was called')
            sock_obj = SocketMock()
            for item in (sock_obj, type(sock_obj)):
                yield item

        def listen(self, arg):
            print(f'function listen was called with {arg} max connections count')

        def send(self, arg):
            arg = arg.decode(settings.ENCODING)
            print(f'function send was called with: \n{arg}')

        def settimeout(self, arg):
            print(f'function settimeout was called with {arg} timeout')

    monkeypatch.setattr(socket, 'socket', SocketMock)


@pytest.fixture
def recv_mock_out_str():
    return {'code': 'zero', "action": 'test', "headers": {'what time is it': '00.00'}, "body": {'message': 'hey, dude!'}}
