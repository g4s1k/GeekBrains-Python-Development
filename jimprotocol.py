#protocol description

import json
import mycssettings as settings
# from contman import DictPackChecker as DPC
# from contman import JsonBytesChecker as JBC
import logging
import carnival
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

    @carnival.log
    def serialise(self):
        try:
            if (self._type == 'client') & ('code' in self._pack.keys()):
                self._pack.pop('code')
            buf_str = json.dumps(self._pack)
            buf_str = buf_str.encode(settings.ENCODING)
            self._pack = zlib.compress(buf_str)
        except:
            errlog.exception('Error occured')
            raise
        # with DPC(self._pack) as temp:
        #     if (self._type == 'client') & ('code' in self._pack.keys()):
        #         temp.buf.pop('code')
        #     print('We are IN')
        #     buf_str = json.dumps(temp.buf)
        #     print(buf_str)
        #     temp.buf = buf_str.encode(settings.ENCODING)
        #     print(temp.buf)
        #     print('code done!!!!!!!!!')
        # print(self._pack)
        return self._pack

    @carnival.log
    def deserialise(self):
        try:
            buf_str = zlib.decompress(self._pack)
            buf_str = buf_str.decode(settings.ENCODING)
            self._pack = json.loads(buf_str)
        except:
            errlog.exception('Error occured')
            raise
        # with JBC(self._pack) as temp:
        #     buf_str = temp.decode(settings.ENCODING)
        #     temp = json.loads(buf_str)
        # return self._pack

    @property
    def pack(self):
        pack = self._pack
        return pack

    @carnival.log
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
        for k, v in body.items():
            yield k, v

    @carnival.log
    def add_command(self, newcommand = {}):
        self._pack['body'].update(newcommand)

    def del_command(self, command_name = {}):
        if command_name in self._pack['body'].keys():
            del self._pack['body'][command_name]
            return True
        else:
            return False

    @carnival.log
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

    @carnival.log
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

    @carnival.log
    def newpack(self, code = 0, action = '', headers = {}, body = {}):
        self._pack = {'code': code, "action": action, "headers": headers, "body": body}
        if self._type == 'client':
            del self._pack["code"]
        elif self._type != 'server':
            print('Invalid pocket type')
            raise TypeError
