import pytest
from Client.Net.myclient import MyClient


@pytest.fixture(params = ['some input', '/dis'], ids = ['some input', '/dis'])
def inputmock(monkeypatch, request):
    def mock_for_input(*args):
        return request.param
    monkeypatch.setattr('builtins.input', mock_for_input)

@pytest.fixture
def entermock(monkeypatch):
    def mock_for_enter_data(self):
        self._dis = True
    monkeypatch.setattr(MyClient, 'enter_data', mock_for_enter_data)

@pytest.fixture
def client_object_control():
    return 'socket object\nclient\nFalse'

@pytest.fixture
def client_object():
    return MyClient()


def test_client_object_initialisation(jimbeam, client_object_control, client_object):
    client = client_object
    control = '\n'.join([client._c_socket.type, client._buf.pocket_type, str(client._dis)])
    assert control == client_object_control

def test_read_data(recv_mock_out_str, client_object):
    client_object.read_data()
    assert client_object._buf.pack == recv_mock_out_str

def test_enter_data(inputmock, client_object):
    client_object.enter_data()
    message = client_object._buf.pack['body']['message']
    if client_object._dis:
        print('/dis command was recieved')
    else:
        assert message == input()

def test_send_data(capsys, client_object):
    client_object._buf.add_message('test')
    client_object.send_data()
    out, err = capsys.readouterr()
    control_set = ('test', 'send')
    for item in control_set:
        assert item in out

def test_connect(entermock, capsys, client_object):
    client_object.connect()
    out, err = capsys.readouterr()
    control_set = ('connect', 'send', 'recv', 'Disconnect')
    for item in control_set:
        assert item in out
