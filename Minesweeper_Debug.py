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
        player_debug.play('random')
        if game_debug.win:
            win_counter+=1
    
    print("Random Choose: {} / {} games won, the winning rate is {}".format(win_counter, retries, win_counter/retries))
    
    win_counter = 0
    for i in range(retries):

        game_debug = Minesweeper_Game.Minesweeper(10,5)
        player_debug = Minesweeper_Agent.Player(agent_host_debug, game_debug)
        player_debug.play('naive')
        if game_debug.win:
            win_counter += 1
    
    print("Naive Choose: {} / {} games won, the winning rate is {}".format(win_counter, retries, win_counter/retries))