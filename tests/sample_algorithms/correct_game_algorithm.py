import os
import sys
sys.path.append(os.getcwd())

from gat_python.game_algorithm import GameAlgorithm


class CorrectGameAlgorithm(GameAlgorithm):
    def process_message(self, message):
        self.send_response('echo: ' + message)


algorithm = CorrectGameAlgorithm()
algorithm.listen()
