# coding: utf-8
from gat_python.python_algorithm import GameAlgorithm


class TrucoAlgorithm(GameAlgorithm):
    def process_message(self, message):
        if message['action'] == 'play':
            self.play(message['context'])
        elif message['action'] == 'accept_truco':
            accept = self.accept_truco(message['context'])
            if accept:
                self.send_response({'action': 'accept_truco'})
            else:
                self.send_response({'action': 'giveup_truco'})

    def play(self, context):
        pass

    def accept_truco(self, context):
        pass

    def upcard(self, card):
        self.send_response({'action': 'upcard', 'hand_card': card})

    def truco(self):
        self.send_response({'action': 'truco'})
