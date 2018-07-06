import logging

deblog = logging.getLogger('deblogger')
errlog = logging.getLogger('errlogger')

class PackChecker():
    def __init__(self, wrap):
        self.save = wrap

    def __enter__(self):
        self.buf = list(self.save)
        return self.buf

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == None:
            self.save[:] = self.buf
        elif exc_type == TypeError:
            errlog.exception('Type error')
        else:
            errlog.exception(f'Error was occured: {exc_type}')
        return True
