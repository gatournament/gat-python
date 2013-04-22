# coding: utf-8
import os
from subprocess import Popen, PIPE, STDOUT

import zmq

import unittest


full_path = os.path.realpath(__file__)
dirpath, filename = os.path.split(full_path)


class IPCTests(unittest.TestCase):
    def algorithm_file(self):
        pass

    def setUp(self):
        port = '88888'
        filepath = os.path.join(dirpath, 'sample_algorithms', self.algorithm_file())
        self.proc = Popen(['python', filepath, port])
        print(filepath, self.proc.poll(), self.proc.pid)
        context = zmq.Context()
        self.sock = context.socket(zmq.REQ)
        self.sock.connect('ipc://localhost:%s' % port)

    def tearDown(self):
        self.sock.close()
        self.proc.kill()


class CorrectGameAlgorithmTests(IPCTests):
    def algorithm_file(self):
        return 'correct_game_algorithm.py'

    def test_send_and_receive_messages_through_ipc(self):
        self.sock.send_string('"msg x"')
        response = self.sock.recv_string()
        self.assertEquals('"echo: msg x"', response)


class BuggedGameAlgorithmTests(IPCTests):
    def algorithm_file(self):
        return 'bugged_game_algorithm.py'

    def test_send_and_receive_messages_through_ipc(self):
        self.sock.send_string('"msg x"')
        response = self.sock.recv_string()
        self.assertEquals('{"error": "runtime error"}', response)
