# coding: utf-8
from functools import update_wrapper
import socket
import sys

import six


try:
    import simplejson as json
except ImportError:
    import json


def encode_object(obj):
    if hasattr(obj, '__getstate__'):
        return obj.__getstate__
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    return obj


def dumps(obj, **kwargs):
    return json.dumps(obj, skipkeys=True, default=encode_object, **kwargs)


def loads(s, **kwargs):
    return json.loads(s, **kwargs)


class GameAlgorithm(object):
    '''
    Usage:

    import os
    import sys
    sys.path.append(os.getcwd())
    algorithm = GameAlgorithm()
    algorithm.listen()
    '''
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None

    def listen(self, host='localhost', port=None):
        if not port:
            port = int(sys.argv[1]) if len(sys.argv) > 1 else 58888
        self.sock.bind((host, port))
        print('Listening %s' % str((host, port)))
        self.sock.listen(1)
        self.conn, addr = self.sock.accept()
        print('Client connected: %s' % str(addr))

        self.stopped = False
        while not self.stopped:
            try:
                self.read_incoming_message()
            except Exception as e:
                print(str(e))
                self.send_error(str(e))
                self.stop()
                six.reraise(*sys.exc_info())
        self.conn.close()

    def stop(self):
        self.stopped = True

    def read_incoming_message(self):
        message = self.conn.recv(8192) # 2**13
        if not message or message == 'stop':
            self.stop()
        else:
            message = loads(message)
            self.process_message(message)

    def process_message(self, message):
        if message['action'] == 'play':
            return self.play(message['context'])

    def play(self, context):
        pass

    def send_response(self, message):
        message = dumps(message)
        message = '%s\n' % message
        if sys.version_info[0] == 2:
            self.conn.sendall(message)
        else:
            self.conn.sendall(bytes(message, 'utf-8'))

    def send_error(self, error_message):
        error = {'error': error_message}
        self.send_response(error)
