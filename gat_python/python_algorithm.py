# coding: utf-8
from functools import update_wrapper
import sys

import six
import zmq

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
        context = zmq.Context()
        self.sock = context.socket(zmq.REP)

    def listen(self, host='localhost', port=None):
        if not port:
            port = sys.argv[1] if len(sys.argv) > 1 else 88888
        self.sock.bind('ipc://%s:%s' % (host, port))
        print('Listening')

        self.stopped = False
        while not self.stopped:
            try:
                self.read_incoming_message()
            except Exception as e:
                print(str(e))
                self.send_error(str(e))
                self.stop()
                six.reraise(*sys.exc_info())

    def stop(self):
        self.stopped = True

    def read_incoming_message(self):
        message = self.sock.recv_string()
        message = loads(message)
        if message == 'stop':
            self.stop()
        self.process_message(message)

    def process_message(self, message):
        if message['action'] == 'play':
            return self.play(message['context'])

    def play(self, context):
        pass

    def send_response(self, message):
        message = dumps(message)
        self.sock.send_string(message)

    def send_error(self, error_message):
        error = {'error': error_message}
        self.send_response(error)
