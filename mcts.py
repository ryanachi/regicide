from math import sqrt, log
from copy import deepcopy
import random

class Node:
    def __init__(self, game, castle, tavern, discard, hand, opp_card,
                 finished, parent, action_index):
        self.children = None  # Dictionary of child nodes
        self.T = 0  # Sum of value of rollouts from this node
        self.N = 0  # Number of visits to this node

        self.game = game  # Copy of the game environment so we can simulate it

        # Sort them since it doesn't matter what order the castle and discard piles
        # are in since they are drawn from mostly randomly as far as the player knows
        self.castle = castle.sort()
        self.tavern = tavern
        self.discard = discard.sort()
        self.hand = hand.sort()
        self.opp_card = opp_card
        
        self.finished = finished  # whether the game is finished or not, so search stops
        self.parent = parent  # for backpropagation
        self.action_index = action_index

        self.c = 1  # Tunable parameter (TODO: change)


    def get_score(self):
        """ Gives values to the node, and MCTS picks nodes with highest value. """

        # Unexplored states have maximum value (favor exploration)
        if self.N == 0:
            return float("inf")
        
        # Need parent node of the current node
        top_node = self
        if self.parent:
            top_node = top_node.parent

        return (self.T / self.N) + self.c * sqrt(log(top_node.N) / self.N)
    

    def create_child(self):
        """ 
        Child node for each possible action from this state. Apply this action to
        a copy of the current node environment and create a child node with that
        action applied
        """

        if self.finished:
            return
        
        actions = []
        games = []

        for c in self.hand:
            actions.append(i)
            new_game = deepcopy(self.game)
            games.append(new_game)

        children = {}
        for action, game in zip(actions,games):
            castle, tavern, discard, hand, opp_card, finished, reward = game.step(action)  # Fix later to fit the actual game
            children[action] = Node(game, castle, tavern, discard, hand, opp_card, finished, self, action)

        self.children = children


    def explore(self):
        """
        Search along tree as follows:
        1. From the current node, continuously (recursively) pick the children which maximize the value 
        2. When a leaf is reached:
            a. If it has never been explored before, do a rollout and update current value
            b. Otherwise, expand the node and create its children. Pick a random child, and do a rollout update
        3. Backpropagate the updated statistics up the tree until the root: update both value and visit counts
        """ 

        current = self
        
        # Step 1:
        while current.children:
            children = current.children
            max_score = max(c.get_score() for c in children.values())
            actions = [a for a, c in children.items() if c.get_score() == max_score]
            if len(actions) == 0:
                print("error zero length", max_score)
            action = random.choice(actions)
            current = children[action]

        # Step 2:
        if current.N >= 1:
            current.create_child()
            if current.children:
                current = random.choice(current.children)
        current.T += current.rollout()
        current.N += 1

        # Step 3:
        parent = current
        while parent.parent:
            parent = parent.parent
            parent.N += 1 
            parent.T += current.T

    def rollout(self):
        """
        Rollout is a random play from a copy of the environment of the current node.  
        Gives value for the current node, which seems random alone. But as number of
        rollouts increase, the more accurate the average of the value.
        """ 

        if self.finished: 
            return 0
        
        v = 0
        finished = False
        new_game = deepcopy(self.game)

        while not finished:
            action = new_game.hand.sample()  # Adjust this later to match our actual game
            castle, tavern, discard, hand, opp_card, finished, reward = new_game.step(action)  # Fix later to fit the actual game
            v += reward
            if finished: # FIX LATER
                #new_game.reset()
                #new_game.close()  --> maybe we do not need these at all. I will leave in for now in case
                break
        
        return v

    def next(self):
        """
        Once search is done, this function defines how to choose the next best action from our current node
        As according to the textbook, algorithm takes the action that maximizes:
            Q(h, a) + c * sqrt(log(N(h))/N(h,a))
        where N(h) = total visit count for all children, N(h, a) is the visit count for the given action, 
        and c is an exploration parameter
        """

        if self.finished:
            raise ValueError("Something is wrong. This game is supposed to be over. Stop playing.")
        
        if not self.child:
            raise ValueError("Something is wrong. You have no children. The game is not over.")
        
        all_N = sum(node.N for node in self.children.values())
        max_val = 0
        max_child = None

        for node in self.children.values():
            val = node.T + self.c * sqrt(log(all_N) / node.N)
            if val > max_val:
                max_val = val
                max_child = node

        return max_child, max_val
