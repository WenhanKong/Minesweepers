import time
from timeit import default_timer as timer
import MalmoPython
import math
import json 
import random

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
        self.teleport_center(x, y, z)
        self.agent_host.sendCommand('attack 1')
        time.sleep(0.7)
        self.agent_host.sendCommand('attack 0')

class Player(Agent):
    # -- the grid for player starts at (1, 228, 1), ends at (size+1, 228, size+1) -- #

    def sweep_random(self):
        while True:
            x = random.randint(0, self.size-1)
            z = random.randint(0, self.size-1)
            if not self.game.board[x][z].visible:
                self.destroy_block(x+1, 228, z+1)
                self.game.sweep(x,z)
                return (x,z)