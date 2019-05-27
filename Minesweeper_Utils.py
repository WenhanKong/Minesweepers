import MalmoPython
import time

def safeStartMission(agent_host, mission, client_pool, recording, role, experimentId):
    used_attempts = 0
    max_attempts = 5
    print("Calling startMission for role", role)
    while True:
        try:
            agent_host.startMission(mission, client_pool, recording, role, experimentId)
            break
        except MalmoPython.MissionException as e:
            errorCode = e.details.errorCode
            if errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_WARMING_UP:
                print("Server not quite ready yet - waiting...")
                time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_INSUFFICIENT_CLIENTS_AVAILABLE:
                print("Not enough available Minecraft instances running.")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait in case they are starting up.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_NOT_FOUND:
                print("Server not found - has the mission with role 0 been started yet?")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait and retry.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            else:
                print("Other error:", e.message)
                print("Waiting will not help here - bailing immediately.")
                exit(1)
        if used_attempts == max_attempts:
            print("All chances used up - bailing now.")
            exit(1)
    print("startMission called okay.")

def safeWaitForStart(agent_hosts):
    print("Waiting for the mission to start", end=' ')
    start_flags = [False for a in agent_hosts]
    start_time = time.time()
    time_out = 120  # Allow two minutes for mission to start.
    while not all(start_flags) and time.time() - start_time < time_out:
        states = [a.peekWorldState() for a in agent_hosts]
        start_flags = [w.has_mission_begun for w in states]
        errors = [e for w in states for e in w.errors]
        if len(errors) > 0:
            print("Errors waiting for mission start:")
            for e in errors:
                print(e.text)
            print("Bailing now.")
            exit(1)
        time.sleep(0.1)
        print(".", end=' ')
    print()
    if time.time() - start_time >= time_out:
        print("Timed out waiting for mission to begin. Bailing.")
        exit(1)
    print("Mission has started.")

def getMissionXML(game):
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
                        <ServerQuitFromTimeUp timeLimitMs="1000"/>
                        <ServerQuitWhenAnyAgentFinishes/>
                    </ServerHandlers>
                </ServerSection>

                <AgentSection mode="Creative">
                    <Name>player</Name>
                    <AgentStart>
                        <Placement x="1" y="229" z="1" pitch="+90" yaw="0"/>
                        <Inventory>
                            <InventoryItem slot="0" type="diamond_pickaxe"/>
                        </Inventory>
                    </AgentStart>
                    <AgentHandlers>
                        <ObservationFromGrid>
                            <Grid name="board" absoluteCoords="1">
                                <min x="1" y="228" z="1"/>
                                <max x="10" y="228" z="10"/>
                            </Grid>
                        </ObservationFromGrid>
                        <MissionQuitCommands/>
                        <AbsoluteMovementCommands/>
                        <ContinuousMovementCommands/>
                        <InventoryCommands/>
                        <AgentQuitFromTouchingBlockType>
                            <Block type="tnt"/>
                        </AgentQuitFromTouchingBlockType>
                    </AgentHandlers>
                </AgentSection>
                </Mission>
                '''
    return mission_xml

def getMissionXMLAfterEnd(game):
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
                        '''+game.drawBoardAfterEnd()+'''
                    </DrawingDecorator>
                    <ServerQuitFromTimeUp timeLimitMs="100000"/>
                    <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
            </ServerSection>

            <AgentSection mode="Creative">
                <Name>player</Name>
                <AgentStart>
                    <Placement x="''' + str(game.size/2) + '" y="260" z="' + str(game.size/2)+ '''" pitch="+90" yaw="0"/>
                </AgentStart>
                <AgentHandlers>
                    <ObservationFromGrid>
                        <Grid name="board" absoluteCoords="1">
                            <min x="1" y="228" z="1"/>
                            <max x="10" y="228" z="10"/>
                        </Grid>
                    </ObservationFromGrid>
                    <MissionQuitCommands/>
                    <AbsoluteMovementCommands/>
                    <ContinuousMovementCommands/>
                    <AgentQuitFromTouchingBlockType>
                        <Block type="tnt"/>
                    </AgentQuitFromTouchingBlockType>
                </AgentHandlers>
            </AgentSection>
            </Mission>
            '''
    return mission_xml