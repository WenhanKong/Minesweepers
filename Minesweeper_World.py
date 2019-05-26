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
#   agent = MinesweeperAgent()
    agent_host_player = MalmoPython.AgentHost()
    agent_host_judge = MalmoPython.AgentHost()


# Use agent_host1 for parsing the command-line options.
# (This is why agent_host1 is passed in to all the subsequent malmoutils calls, even for
# agent 2's setup.)
    malmoutils.parse_command_line(agent_host_player)

# -- set up the game -- #
    game = Minesweeper_Game.Minesweeper(10, 5)
    player = Minesweeper_Agent.Player(agent_host_player, game.size)
    judge = Minesweeper_Agent.Judge(agent_host_judge, game.size)
    #game.play()

# -- set up mission XML -- #
    mission_xml='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <About>
                    <Summary>Minesweeper World Gnerator.</Summary>
                </About>
  
                <ServerSection>
                    <ServerInitialConditions>
                        <Time><StartTime>1000</StartTime></Time>
                        <Weather>clear</Weather>
                    </ServerInitialConditions>
                    <ServerHandlers>
                    <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1"/>
                    <DrawingDecorator>
                        '''+game.drawBoard()+'''
                    </DrawingDecorator>
                    <ServerQuitFromTimeUp timeLimitMs="100000"/>
                    <ServerQuitWhenAnyAgentFinishes/>
                    </ServerHandlers>
                </ServerSection>

                <AgentSection mode="Survival">
                    <Name>player</Name>
                    <AgentStart>
                        <Placement x="1" y="229" z="1" pitch="0" yaw="0"/>
                    </AgentStart>
                    <AgentHandlers>
                        <ObservationFromGrid>
                            <Grid name="board" absoluteCoords="1">
                                <min x="1" y="228" z="1"/>
                                <max x="10" y="228" z="10"/>
                            </Grid>
                        </ObservationFromGrid>
                        <AbsoluteMovementCommands/>
                        <ContinuousMovementCommands/>
                        <AgentQuitFromTouchingBlockType>
                            <Block type="tnt"/>
                        </AgentQuitFromTouchingBlockType>
                    </AgentHandlers>
                </AgentSection>

                <AgentSection mode="Creative">
                    <Name>judge</Name>
                    <AgentStart>
                        <Placement x="12" y="228" z="12" pitch="+90" yaw="0"/>
                    </AgentStart>
                    <AgentHandlers>
                        <ObservationFromGrid>
                            <Grid name="board" absoluteCoords="1">
                                <min x="1" y="227" z="1"/>
                                <max x="10" y="228" z="10"/>
                            </Grid>
                        </ObservationFromGrid>
                        <DiscreteMovementCommands/>
                        <AbsoluteMovementCommands/>
                    </AgentHandlers>
                </AgentSection>
                
                </Mission>
                '''

    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    my_mission_record = MalmoPython.MissionRecordSpec()

    client_pool = MalmoPython.ClientPool()
    client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )
    client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10001) )

    Minesweeper_Utils.safeStartMission(agent_host_player, my_mission, client_pool, my_mission_record, 0, '' )
    Minesweeper_Utils.safeStartMission(agent_host_judge, my_mission, client_pool, my_mission_record, 1, '' )
    Minesweeper_Utils.safeWaitForStart([agent_host_player, agent_host_judge])    

    world_state = agent_host_judge.getWorldState()
    # perform a few actions
    while game.end == False:
        msg = world_state.observations[-1].text
        observations = json.loads(msg)
        grid = observations.get(u'board', 0)
        bottom_layer = grid[:len(grid)//2]
        top_layer = grid[len(grid)//2:]

        player.observe(top_layer)
        player_x, player_z = player.choose_random()
        time.sleep(0.5)

        game.sweep(player_x, player_z)

        judge.observe(top_layer)
        judge.updateBoardStatus(game.board)

    # wait for the missions to end    
    while agent_host_player.peekWorldState().is_mission_running or agent_host_judge.peekWorldState().is_mission_running:
        time.sleep(1)
        world_state = agent_host_judge.getWorldState()

        #if world_state.number_of_observations_since_last_state > 0:

    

    #Minesweeper_Agent.teleport(agent_host_player, 6, 229, 6)
    #Minesweeper_Agent.act(agent_host_player, player_x, 229, player_z)

            
    for error in world_state.errors:
        print("Error:",error.text)

    print()
    print("Mission ended")