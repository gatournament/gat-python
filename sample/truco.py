import random
from gat_python import TrucoAlgorithm

class YourAlgorithm(TrucoAlgorithm):
    def play(self, context):
        """
        You must decide which card of your hand you want to upcard in the table.
        And you can truco too.
        """
        print(context) # to see all information you have to take your decision

        randomDecisionToTruco = random.randint(0, 10) > 5
        if self.can_truco(context) and randomDecisionToTruco:
            return self.truco() # only call this method if self.can_truco(context) returns True
        else:
            hand = context['hand']['cards']
            random_card = hand[random.randint(0, len(hand)-1)]
            return self.upcard(random_card)

    def accept_truco(self, context):
        """
        @return True or False
        """
        return random.randint(0, 1) == 1

# Required:
algorithm = YourAlgorithm()
algorithm.listen()