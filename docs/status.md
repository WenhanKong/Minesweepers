---
layout: default
title:  Status
---

## Project Summary
It's a minesweeper solver! It can solve any board, with any size, and exactly compute every cell's chance of being a mine. It achieves this through advanced combinatorial and probability analysis with artificial intelligence. The project will use random search as the baseline algorithm, naive search as the intermediate algorithm and Q-Learning as the advancing algorithm.   

### What is Minesweeper?
Just in case you don't know how the game works: Minesweeper is a single-player puzzle game avaliable on several avaliable operating systems and GUIs. At the start of the game, the player receives a ![equation](https://latex.codecogs.com/png.latex?n&space;\times&space;m) rectangular grid of covered cells. Each turn, player may probe or uncover a cell revealing either a mine or an integer. This integer indicates the number of mines adjacent to the particular cell. As such, the number ranges from 0 to 8, since it's impossible for a cell to have more than eight neighbors. The game ends when player probes a cell containing a mine (lose), or uncovered every cell that does not contain a mine (win).
### Game Setup:
   Board With Cover        |  Board Without Cover
:-------------------------:|:-------------------------:
<img src="images/board_with_cover.png" width="450"/>  |  <img src="images/board_without_cover.png" width="450"/>


## Approach

![white_wool](/docs/images/0.png)  *Random Search*

