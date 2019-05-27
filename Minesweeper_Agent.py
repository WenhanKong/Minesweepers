import time
from timeit import default_timer as timer
import MalmoPython
import math
import json 
import random
import operator

class Agent(object):
    def __init__(self, agent_host, game): 
        
        self.size = game.size    
        self.grid = ['glass'] * self.size * self.size
        self.agent_host = agent_host
        self.game = game

    def teleport(self, teleport_x, teleport_y, teleport_z):
        """Directly teleport to a specific position."""
        tp_command = "tp " + str(teleport_x)+ " " + str(teleport_y) + " " + str(teleport_z)
        self.agent_host.sendCommand(tp_command)

    def teleport_center(self, teleport_x, teleport_y, teleport_z):
        """Directly teleport to the center of a block."""
        tp_command = "tp " + str(teleport_x+0.5)+ " " + str(teleport_y) + " " + str(teleport_z+0.5)
        self.agent_host.sendCommand(tp_command)

    def destroy_block(self, x, y, z):
        time.sleep(0.5)
        self.teleport_center(x, y+1, z)
        time.sleep(0.1)
        self.agent_host.sendCommand('attack 1')
        time.sleep(0.2)
        self.agent_host.sendCommand('attack 0')

class Player(Agent):
    # -- the grid for player starts at (1, 228, 1), ends at (size+1, 228, size+1) -- #
    
    def __init__(self, agent_host, game):
        Agent.__init__(self, agent_host, game)
        # -- dictionary object that stores {(x,y):proba as mine }
        self.board_with_prob = dict()
        for row in range(self.size):
            for col in range(self.size):
                self.board_with_prob[(row, col)] = 0
        #print(self.board_with_prob)

    def sweep_random(self):
        while True:
            x = random.randint(0, self.size-1)
            z = random.randint(0, self.size-1)
            if not self.game.board[x][z].visible:
                self.destroy_block(x+1, 228, z+1)
                self.game.sweep(x,z)
                return (x,z)

    def sweep_naive(self):
        while True:
            x, z = self.choose_naive()
            if not self.game.board[x][z].visible:
                self.destroy_block(x+1, 228, z+1)
                time.sleep(1)
                self.game.sweep(x,z)
                self.game.checkWinCondition()
                return (x,z)

    # -- naive search surrounding non-visible and legal tiles, calculate each tile's probabilitity as mine, return position with the lowest value-- #
    def choose_naive(self):
        res = {}
        for row in range(self.size):
            for col in range(self.size):
                currentTile = self.game.board[row][col]
                if currentTile.visible and currentTile.counter > 0:
                    nearby_counter = 0
                    for (dx, dy) in self.game.directions:
                        if self.game.inbounds(row+dx, col+dy):
                            nearbyTile = self.game.board[row+dx][col+dy]
                            nearby_counter+=1
                            if not nearbyTile.visible:
                                if not res.get((row+dx, col+dy)):
                                    res[(row+dx, col+dy)] = currentTile.counter/nearby_counter
                                else:
                                    res[(row+dx, col+dy)]+=currentTile.counter/nearby_counter
        #print(res)
        if res.items():
            return min(res.items(), key=operator.itemgetter(1))[0]
        else:
            #print("the dict is empty")
            return self.choose_random()

    # -- for debug -- #

    def play(self, choose):
        while not self.game.end:
            #print("=================== Board Before =====================")
            #self.game.printBoard()
            #print(self.board_with_prob)

            if choose == 'naive':
                (row, col) = self.choose_naive()
            #print(row, col)
            elif choose == 'random':
                (row, col) = self.choose_random()
            self.game.sweep(row, col)

            #print("=================== Board After =====================")
            #self.game.printBoard()
            #print(self.board_with_prob)

        #print("++++++++++++++++++++ Game End +++++++++++++++++++++")

    def choose_random(self):
        while True:
            x = random.randint(0, self.size-1)
            z = random.randint(0, self.size-1)
            if not self.game.board[x][z].visible:
                return (x,z)


class Judge(Agent):

    pass