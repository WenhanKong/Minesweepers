from __future__ import division
#import numpy as np
import Minesweeper_Game
import Minesweeper_Utils
import Minesweeper_Agent
import MalmoPython
import malmoutils

import os
import random
import sys
import time
import json
import random
import math
import errno
import uuid
from collections import defaultdict, deque
from timeit import default_timer as timer


if __name__ == '__main__':

    # -- set up mission agent -- #
    agent_host_player = MalmoPython.AgentHost()
    client_pool = MalmoPython.ClientPool()
    client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )

    # Use agent_host_player for parsing the command-line options.
    malmoutils.parse_command_line(agent_host_player)

    # -- set up the game -- #
    # Minesweeper(size, num_mines)
    game = Minesweeper_Game.Minesweeper(10, 5)
    player = Minesweeper_Agent.Player(agent_host_player, game)
    
    # -- while the game is not end, keep asking player to randomly choose a tile to sweep and update mission xml for next turn -- #
    while not game.end:
        mission_xml = Minesweeper_Utils.getMissionXML(game)
    
        my_mission = MalmoPython.MissionSpec(mission_xml, True)
        my_mission_record = MalmoPython.MissionRecordSpec()

        time.sleep(1)  
        Minesweeper_Utils.safeStartMission(agent_host_player, my_mission, client_pool, my_mission_record, 0, '' )
        Minesweeper_Utils.safeWaitForStart([agent_host_player])

        print("========================================================")
    
        # -- get world state -- #
        world_state = agent_host_player.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = agent_host_player.getWorldState()
        
        # -- player random choose a position to sweep -- #
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            observations = json.loads(msg)
            grid = observations.get(u'board', 0)

            # -- randomly choose a tile to sweep and update board status -- #
            #game.printBoard()
            # -- if the tile is a mine, game.end will be set to True
            x,z = player.sweep_random()
            print(x, z)
            print("========================================================")
            #game.printBoard()
            
        for error in world_state.errors:
            print("Error:",error.text)

        time.sleep(1)
        print()
        print("The round end")

    # -- after the game is end, minecraft shows a complete board status without cover blocks -- #
    print("Full Board Stats")
    mission_xml = Minesweeper_Utils.getMissionXMLAfterEnd(game)
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    my_mission_record = MalmoPython.MissionRecordSpec()
    time.sleep(1)
    Minesweeper_Utils.safeStartMission(agent_host_player, my_mission, client_pool, my_mission_record, 0, '' )
    Minesweeper_Utils.safeWaitForStart([agent_host_player]) 