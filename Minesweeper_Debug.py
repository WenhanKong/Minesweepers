import Minesweeper_Agent
import Minesweeper_Game
import MalmoPython


if __name__ == '__main__':
    agent_host_debug = MalmoPython.AgentHost()

    retries = 10
    win_counter = 0
    for i in range(retries):

        game_debug = Minesweeper_Game.Minesweeper(10, 5)
        player_debug = Minesweeper_Agent.Player(agent_host_debug, game_debug)
        player_debug.play()
        if game_debug.win:
            win_counter+=1
    
    print("{} / {} games won".format(win_counter, retries))
            