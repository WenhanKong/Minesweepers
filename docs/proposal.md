---
layout: default
title:  Proposal
---


## Summary of the Project
Our project explores the challenges associated with designing a Minesweeper solving algorithm in Minecraft. It considers how to start a game for more a advancing situation, to modify various heuristics for handling guesses, and to make deterministic deductions with different strategies.   
 
<p align="center">
<img src="docs/images/minesweep_board.png" width="250"/>  
</p>

Above is a typical minesweeping gameboard. Playing the Minesweeper requires a fair amount of logic. When a player tries to uncover every square that does not contain a mine, it is a clever move to use the numbered square to deduce the location of mines.
Our AI agent's actions can be categorized into three:
+ Read the board.
+ Compute.
+ Make changes to the board.  

We assume that the AI agent takes the gameboard as the input and knows the whole state of the world. After computation, the AI agent can make the best decision on marking potential mine blocks as the output. 

## AI/ML Algorithms
We are using Contraint Satisfaction Problem Model with Backtracking for our project. 

## Evaluation Plan
We are using three metrics to test how well our AI agent perform in Minesweeper:
+ the testing accuracy
+ the average percentage of board uncovered
+ the winning rate  

The baseline is brute force computation with random guessing. In terms of winning rate, We expect that our approach can achieve 70% win rate which is much higher than the rate of baseline. 

In qualitative analysis, having multiple games allows for computing the average winning rate as well as the standtard deviation. We beleive that the win ratio is the most straightforward measurement for determining how good our approach is. The expected number of guesses is also essential to consider, since it often relates to the time and space usage. We may use matplot to visualize relationships between metrics. 
## Appointment with the Instructor 
2019-May-8-16:00
