import pytest
from myserver import MyServer
import socket
from jimprotocol import JimPocket


@pytest.fixture
def check_list_for_init():
    return 'Socket', 'bind', '{}', 'deque([])', 'settimeout', 'JimPocket', 'server', 'False'

@pytest.fixture
def serv_obj():
    return MyServer()

@pytest.fixture
def check_accept():
    return type(socket.socket())

@pytest.fixture
def sock_obj():
    return socket.socket()

@pytest.fixture
def send_check_list():
    return 'send', '200'

@pytest.fixture
def stop_caster(monkeypatch):
    def blind_look(self, atr):
        self.stop()
    monkeypatch.setattr(MyServer, 'look', blind_look)

@pytest.fixture
def serv_start_check_list():
    return 'listen', 'accept', 'recv', 'send', 'Server stopped'


def test_serv_obj_init(jimbeam, capsys, check_list_for_init):
    serv = MyServer()
    print(f'{serv._stop}, {serv._requests_list}, {serv._connections_list}')
    out, err = capsys.readouterr()
    for check_item in check_list_for_init:
        assert check_item in out

def test_accept_connection(serv_obj, check_accept):
    serv_obj.accept_connection()
    d = serv_obj._connections_list
    assert check_accept in d.values()

def test_read_data(serv_obj, recv_mock_out_str, sock_obj):
    serv_obj.read_data(sock_obj)
    recieved_pack = serv_obj._requests_list.popleft()
    assert recieved_pack.pack == recv_mock_out_str

def test_echo_server_send_data(serv_obj, sock_obj, capsys, send_check_list):
    serv_obj.read_data(sock_obj)
    serv_obj.send_data(sock_obj, serv_obj._buf)
    out, err = capsys.readouterr()
    for check_item in send_check_list:
        assert check_item in out

def test_stop(serv_obj):
    serv_obj.stop()
    assert serv_obj._stop == True

def test_look(serv_obj):
    pack = JimPocket('client')
    pack.add_command({'newcommand': '/stop'})
    serv_obj.look(pack)
    assert serv_obj._stop == True

def test_start(serv_obj, stop_caster, serv_start_check_list, capsys):
    serv_obj.start()
    out, err = capsys.readouterr()
    for check_item in serv_start_check_list:
        assert check_item in out
