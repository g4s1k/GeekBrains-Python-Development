class DictPackChecker():
    def __init__(self, pack):
        self.pack = pack
        print('Hi, i\'m contman!')

    def __enter__(self):
        self.buf = dict(self.pack)
        print('Contman setup done')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == None:
            self.pack = self.buf
            print(self.pack)
            print('contman teardown done')
        elif exc_type == TypeError:
            print('Invalid type recieved')
        else:
            print(f'Error was occured: {exc_type}')
        return True


class JsonBytesChecker():
    def __init__(self, pack):
        self.pack = pack


    def __enter__(self):
        self.buf = bytes(self.pack)
        return self.buf

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == None:
            self.pack = self.buf
        elif exc_type == TypeError:
            print('Invalid type recieved')
        else:
            print(f'Error was occured: {exc_type}')
        return True