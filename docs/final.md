---
layout: default
title:  Final Report
---

## Video
<iframe width="1000" height="1000" src="https://www.youtube.com/embed/9xKekrs3NvA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>  

## Project Summary
It's a minesweeper solver! It can solve any board, with any size, and exactly compute every cell's chance of being a mine. It achieves this through advanced combinatorial and probability analysis with artificial intelligence. The project will use random search as the baseline algorithm, naive search as the intermediate algorithm and Q-Learning as the advancing algorithm.   

### What is Minesweeper?
Just in case you don't know how the game works: Minesweeper is a single-player puzzle game avaliable on several avaliable operating systems and GUIs. At the start of the game, the player receives a ![equation](https://latex.codecogs.com/png.latex?n&space;\times&space;m) rectangular grid of covered cells. Each turn, player may probe or uncover a cell revealing either a mine or an integer. This integer indicates the number of mines adjacent to the particular cell. As such, the number ranges from 0 to 8, since it's impossible for a cell to have more than eight neighbors. The game ends when player probes a cell containing a mine (lose), or uncovered every cell that does not contain a mine (win).
#### Game Setup:

|   Board With Cover        |  Board Without Cover      |
|:-------------------------:|:-------------------------:|
|<img src="images/board_with_cover.png" width="450"/>  |  <img src="images/board_without_cover.png" width="450"/>|
  
  
  
## Approaches

![lime_wool](images/736.png)  **_Random Search_**  
  
You might realize that this is basically the most stupid way to find solution to the game.  
Data for random search approach is generated in the following manner. Each tile in the game board is a Tile class. All the tiles are stored in a 2-dimensional list, and their locations, in terms of row and column, are represetned by list index. 
Random search will keep generating two random integer as the location of next tile to be uncovered until the tile is guaranteed to be inside the board and staying covered. 
```
#Alogrithm 1 sweep_random
while not game over do:
   while True:
      randomly select a tile
      if the tile is covered and the cell is inside the board:
         sweep the tile
         return the tile's location
      end if
end while
```

![orange wool](images/1.png)  **_Naive Search_**

  
Data for Naive search approach is generated in the following manner. Each tile can be represented as a feature with an integer determined by the tile state in current board. If the tile is uncovered, the corresponding feature is represented by the number of mines to which the square is adjacent. The integer value is stored in _tile_ class as _COUNTER_ attribute. If the tile is uncovered, _COUNTER_ attribute will be set to 0 by default since it does not provide any information. And the _tile_ class also stores whether the tile is visible to the player with an _visible_ value.  

<p align="center"> 
<img src="https://i.imgur.com/41QOe.png">
</p>

At each state the game, the naive search stores all tiles that are not visible, but are adjacent to visible tiles in perimeter. Moves are chosen randomly from tiles within the perimeter with some fixed probability, and otherwise just use random search. This method models normal game play where most moves are selected from the perimeter of the current board. However, our algorithms do not flag tiles indicating a mine is present like in real life; they only predict whether a tile is suitable to be a next move. The general greedy algorithm for naive_search is presented below:

```
while not game over do:
   for all the tiles in the current board:
      if the tile is invisible and the tile is adjacent to visible tiles:
         add the tile to primeter
         get surronding tiles of the current tile
         calculate probability of the current tile being a mine
      end if
   choose a tile with minimum probability of being a mine. 
   sweep the tile
end while
```
![pink wool](images/6.png)  **_Q-Learning_**

One approach is to model Minesweeper game as an Markov Decision Process and use a modified version of Q-Learning to discover the best moves for each given board state. After learning the Q values, the algorithm would then use rewards obtained to play the game. 

<p align="center"> 
<img src="images/Q-Learning_function.png">
</p>

This is a standard Q-Learning algorithm form. This function allows the algorithm to learn not just about the direct reward of a particular action, but also a particular action is more likely to lead to reward in a long-term. However, while common chess games are more concerned with endgame result, minesweeper is more interested in intermediate reward: whether the tile contains a mine. Therefore, to better approximate this reward, we remove dicount factor and estimate of optimal future value:

<p align="center"> 
<img src="https://latex.codecogs.com/png.latex?$&space;\widehat&space;{&space;Q&space;}&space;^&space;{&space;new&space;}&space;(&space;s_t&space;,&space;a_t&space;)&space;\leftarrow&space;(&space;1&space;-&space;\alpha&space;)&space;\cdot&space;\hat&space;{&space;Q&space;}&space;^&space;{&space;old}&space;(&space;s_t&space;,&space;a_t&space;)&space;&plus;&space;\alpha&space;\cdot&space;(&space;r_t&space;)$">
</p>

By giving reward for choosing a mine tile to be a negative number (for example, -1), and that of choosig a non-mine tile to be a positive numebr(1), we are able to find the tile which is least likely to be a mine with the highest Q value.

```
while not game over do:
   s = current state of the board
   sweep at random location
   if tile is mine:
      r = -1
   else:
      r = 1
   end if 
   Q(s,a) = (1-alpha)*Q(s,a) + alpha(r)
end while
```

## Evaluation
Three approaches are tested on two boards with different size and mine density.

![blue wool](images/3.png)  **_Win Rate_**  
We use win rate as the most important metric to understand how our approaches perform in playing Minesweeper:

<p align="center">
  <img src="images/boardsize-winrate.png" width="1000" />
</p>

In the 4x4 board with 3 mines, all approaches except random choose exhibit moderate success; the Q-Learning approaches with almost 80% accuracy.
However, the performance of three approaches drops after the board size increases. This is reasonable since, when playing Minesweeper, the game will automatically flip any adjcent non-mine tiles. Larger game board also means more chances to make decision. For method like random choose, it is almost impossible for it to consecutively choose correct tiles. 
As shown above, for a board larger than 5x5, it becomes harder for all approches to have satisfied probability of correct guess. 

![red_wool](images/7.png)  **_Number of Mines_**
<p align="center">
  <img src="images/winrate-nummines.png" width="1000" />
</p>

The result shows that the win rate drops quickly with increasing mine density: a game with higher mine density is simply harder to win because a board with more mines has far more layouts. Consider a board with size ![](https://latex.codecogs.com/png.latex?n&space;\times&space;n) and p mines in total, where ![](https://latex.codecogs.com/png.latex?p<n^{2}). On this board, the total number of distinct configurations equals to ![](https://latex.codecogs.com/png.latex?\frac&space;{&space;n&space;^&space;{&space;2&space;}&space;!&space;}&space;{&space;p&space;!&space;(&space;n&space;-&space;p&space;)&space;!&space;}). A greater number of possible board configurations means a more chanllenging game because it creates a huge state space that makes every move less certain. 

![yellow_wool](images/4.png) **_Number of Training_**

<p align="center">
  <img src="images/training-winrate.png" width="1000" />
</p>

While Q-learning shows the best result, it also suffers from its large state space. On a Minesweeper game board, each tile can hold 9 possible values (0-8 for counter, 9 for invisible). Thus the upper bond for total game board configurations is ![](https://latex.codecogs.com/png.latex?9^{mn}). While in reality the true number of possible game configurations is smaller (due to of large number of inconsistent boards), the number still proves that the state space of Q-learning explodes when the board size increases. Also, for the same state visited before, it is possible that mines hide under different tiles, so we must visit a state many times in order to accurately approximate the probability of whether each tile is not a mine. 


## References

see [/docs/references](https://github.com/WenhanKong/Minesweepers/edit/master/docs/references)  

Charts are made in (https://www.rapidtables.com)  
Block images are provided by (https://www.minecraftinfo.com)  
Video is made by iMovie and QuickTimePlayer    
