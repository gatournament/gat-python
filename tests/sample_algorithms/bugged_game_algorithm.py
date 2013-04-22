import os
import sys
sys.path.append(os.getcwd())

from gat_python.python_algorithm import GameAlgorithm


class BuggedGameAlgorithm(GameAlgorithm):
    def process_message(self, message):
        raise Exception('runtime error')


algorithm = BuggedGameAlgorithm()
algorithm.listen()
