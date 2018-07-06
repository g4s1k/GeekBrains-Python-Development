#protocol description

import json
import netsettings as settings
from Server.contman import PackChecker
import logging
import zlib


deblog = logging.getLogger('deblogger')
errlog = logging.getLogger('errlogger')


class JimPocket:

    def __init__(self, pocket_type = '', code = 0, action = '', headers = {}, body = {}):
        self._pack = {'code': code, "action": action, "headers": headers, "body": body}
        self._type = pocket_type.lower()
        if self._type == 'client':
            del self._pack["code"]
        elif self._type != 'server':
            print('Invalid pocket type')
            raise TypeError

    def serialise(self):
        wrap = [self._pack]
        with PackChecker(wrap) as wrap_copy:
            data_copy = wrap_copy[0]
            if (self._type == 'client') & ('code' in self._pack.keys()):
                data_copy.pop('code')
            buf_str = json.dumps(data_copy)
            buf_str = buf_str.encode(settings.ENCODING)
            wrap_copy[0] = zlib.compress(buf_str)
        self._pack = wrap[0]
        return self._pack

    def deserialise(self):
        wrap = [self._pack]
        with PackChecker(wrap) as wrap_copy:
            data_copy = wrap_copy[0]
            buf_str = zlib.decompress(data_copy)
            buf_str = buf_str.decode(settings.ENCODING)
            wrap_copy[0] = json.loads(buf_str)
        self._pack = wrap[0]
        return self._pack

    @property
    def pack(self):
        pack = self._pack
        return pack

    def pack_it(self, data):
        self._pack = data

    @property
    def action(self):
        action = self._pack.get('action')
        return action

    def set_action(self, action = ''):
        self._pack.update({'action': action})

    @property
    def headers(self):
        headers = self._pack.get('headers')
        for k, v in headers.items():
            yield k, v

    def add_header(self, newheader = {}):
        self._pack['headers'].update(newheader)

    def del_header(self, header_name = ''):
        if header_name in self._pack['headers'].keys():
            del self._pack['headers'][header_name]
            return True
        else:
            return False

    @property
    def body(self):
        body = self._pack.get('body')
        return body

    def add_command(self, newcommand = {}):
        self._pack['body'].update(newcommand)

    def del_command(self, command_name = {}):
        if command_name in self._pack['body'].keys():
            del self._pack['body'][command_name]
            return True
        else:
            return False

    def add_message(self, message = ''):
        if 'message' not in self._pack['body'].keys():
            self._pack['body'].update({'message': message})
        else:
            _buf_str = self._pack['body']['message']
            _buf_str = '\n'.join([_buf_str, message])
            self._pack['body'].update({'message': _buf_str})

    def del_message(self):
        del self._pack['body']['message']

    @property
    def code(self):
        code = self._pack.get('code')
        return code

    def set_code(self, code = 0):
        if 'code' not in self._pack:
            buf = {}
            buf.update({'code': code})
            buf.update(self._pack)
            self._pack = buf
        else:
            self._pack.update({'code': code})

    def show_pack(self):
        buf_str = ''
        for item in self._pack:
            if type(self._pack[item]) is not dict:
                buf_str = '\n'.join([buf_str, f'{item}: {self._pack[item]}'])
            else:
                buf_str = '\n'.join([buf_str, item])
                for subitem in self._pack[item]:
                    buf_str = '\n'.join([buf_str, f'      {subitem}: {self._pack[item][subitem]}'])
        print(buf_str)

    def newpack(self, code = 0, action = '', headers = {}, body = {}):
        self._pack = {'code': code, "action": action, "headers": headers, "body": body}
        if self._type == 'client':
            del self._pack["code"]
        elif self._type != 'server':
            print('Invalid pocket type')
            raise TypeError
