import Minesweeper_Agent
import Minesweeper_Game
import MalmoPython


if __name__ == '__main__':
    agent_host_debug = MalmoPython.AgentHost()

    retries = 1
    win_counter = 0

    qlearner = Minesweeper_Agent.Qlearner(agent_host_debug)
    qlearner.train2(num_simulations=10000000, grid_size=5, reward=1, game_size=5, num_mines=5)
    qmap = qlearner.get_qmap()

    
    for i in range(retries):
        game_debug = Minesweeper_Game.Minesweeper(5,5)
        qplayer_debug = Minesweeper_Agent.Player(agent_host_debug, game_debug)

        # -- first move: randomly choose -- #
        qplayer_debug.sweep_random()
        #print("=============Full Board Before Game================")
        #game_debug.printFullBoard()
        
        while not game_debug.end:
            game_debug.printBoard()
            current_state = game_debug.get_current_state()
            frontier = Minesweeper_Agent.get_frontier_by_state(current_state, game_debug.size)

            best_action = Minesweeper_Agent.choose_action_with_highest_Q2(qmap, current_state, frontier)
            row, col = best_action
            game_debug.sweep(row, col)


        #print("============= Board After Game ================")
        #game_debug.printBoard()
        game_debug.checkWinCondition()
        if game_debug.win:
            win_counter+=1
    
        print("Q Choose: {} / {} games won, the winning rate is {}".format(win_counter, retries, win_counter/retries))

    """
    for i in range(retries):

        game_debug = Minesweeper_Game.Minesweeper(10, 5)
        player_debug = Minesweeper_Agent.Player(agent_host_debug, game_debug)
        player_debug.play('random')
        if game_debug.win:
            win_counter+=1
    
    print("random Choose: {} / {} games won, the winning rate is {}".format(win_counter, retries, win_counter/retries))
    
    win_counter = 0
    for i in range(retries):

        game_debug = Minesweeper_Game.Minesweeper(10,5)
        player_debug = Minesweeper_Agent.Player(agent_host_debug, game_debug)
        player_debug.play('naive')
        if game_debug.win:
            win_counter += 1
    
    print("Naive Choose: {} / {} games won, the winning rate is {}".format(win_counter, retries, win_counter/retries))

    """