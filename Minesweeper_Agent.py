import time
from timeit import default_timer as timer
import MalmoPython
import math
import json 
import random

class Agent(object):
    def __init__(self, agent_host, size): 
        
        self.size = size    
        self.grid = ['glass'] * size * size
        self.agent_host = agent_host

    def observe(self, grid):
        self.grid = grid

    def teleport(self, teleport_x, teleport_y, teleport_z):
        """Directly teleport to a specific position."""
        tp_command = "tp " + str(teleport_x)+ " " + str(teleport_y) + " " + str(teleport_z)
        self.agent_host.sendCommand(tp_command)

    def act(self, x, y, z):
        self.teleport(x, y, z)
        self.agent_host.sendCommand("setPitch 90")
        self.agent_host.sendCommand("attack 1")
        time.sleep(0.8)
        self.agent_host.sendCommand("attack 0")

class Player(Agent):
    #the grid for player starts at (1, 228, 1), ends at (size+1, 228, size+1)

    def choose_random(self):
        ''' randomly choose a glass block to sweep '''
    #    print(self.grid)
        while True:
            x = random.randint(0, self.size-1)
            z = random.randint(0, self.size-1)
            #print(x,z)
            if self.grid[(z*self.size + x)] == 'glass':
                #the board start at (1,1), all coords need to plus 1
                self.act(x+1,229,z+1)
                return (x,z)

class Judge(Agent):

    def updateBoardStatus(self, board):
        for z in range(self.size):
            for x in range(self.size):
                currentTile = board[z][x]
                if currentTile.visible and self.grid[z*self.size + x] == 'glass':
                    self.act(x+1, 229, z+1)