import json
import pytest
from jimprotocol import JimPocket
import mycssettings as settings


@pytest.fixture
def pack_example():
    return {'code': 'zero', "action": 'test', "headers": {'what time is it': '00.00'}, "body": {'message': 'hey, dude!'}}

@pytest.fixture
def unpacked_pack():
    up = '\ncode: zero\naction: test\nheaders\n      what time is it: 00.00\nbody\n      message: hey, dude!'
    return up

@pytest.fixture
def serialised(pack_example):
    buf = json.dumps(pack_example)
    return buf.encode(settings.ENCODING)

@pytest.fixture
def pocket(pack_example):
    return JimPocket('server', **pack_example)

@pytest.fixture
def action():
    return 'act'

@pytest.fixture
def code():
    return 777

@pytest.fixture
def header():
    return {'header': 'head'}

@pytest.fixture
def command():
    return {'attack': 'Nexus'}

@pytest.fixture
def message():
    return 'Hello everyone!'


def test_pack(pocket, pack_example):
    assert pocket.pack == pack_example

def test_pack_it(pocket, pack_example):
    pocket.pack_it(pack_example)
    assert pocket.pack == pack_example

def test_serialise(pocket, serialised):
    result = pocket.serialise()
    assert result == serialised

def test_deserialise(pocket, pack_example, serialised):
    pocket.pack_it(serialised)
    result = pocket.deserialise()
    assert result == pack_example

def test_set_action(pocket, action):
    pocket.set_action(action)
    assert pocket.action == action

def test_add_header(pocket, header):
    pocket.add_header(header)
    headers = pocket.headers
    assert all(item in headers for item in header.items())

def test_del_header(pocket, header):
    pocket.add_header(header)
    pocket.del_header(*header)
    headers = pocket.headers
    assert all(item not in headers for item in header.items())

def test_add_command(pocket, command):
    pocket.add_command(command)
    body = pocket.body
    assert all(item in body for item in command.items())

def test_del_command(pocket, command):
    pocket.add_command(command)
    pocket.del_command(*command)
    body = pocket.body
    assert all(item not in body for item in command.items())

def test_del_message(pocket):
    pocket.del_message()
    body_keys = pocket.pack['body'].keys()
    assert 'message' not in body_keys

def test_add_message_upd(pocket, message, pack_example):
    one = pack_example['body']['message']
    two = '\n'.join([one, message])
    pocket.add_message(message)
    get = dict(pocket.body)
    text = get['message']
    assert text == two

def test_code(pocket, pack_example):
    assert pocket.code == pack_example['code']

def test_set_code_ex(pocket, code):
    pocket.set_code(code)
    assert pocket.code == code

def test_set_code_dex(pocket, code):
    del pocket._pack['code']
    pocket.set_code(code)
    assert pocket.code == code

def test_show_pack(pocket, unpacked_pack, capsys):
    pocket.show_pack()
    out, err = capsys.readouterr()
    assert unpacked_pack in out

def test_newpack(pocket, code, action, header, command):
    pocket.newpack(code, action, header, command)
    com = {'code': code, "action": action, "headers": header, "body": command}
    assert pocket.pack == com
