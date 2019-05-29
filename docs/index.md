---
layout: default
title:  Home
---

Source code: https://github.com/WenhanKong/Minesweepers

Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)


<p float="left">
  <img src="https://exceptionnotfound.net/content/images/2016/04/minesweeper-intro.png" width="300" />
  <img src="/docs/images/board_without_cover.png" width="500" height="300"/> 
</p>


Welcome to the world of minesweepers! It is one of the most classic games of all time, and although I can't find it anymore on my professional gaming computer, oh my I miss the days I played it on those huge heavy old PCs as one of the only games on Windows98 or Windows2000.

If you don't know who we are, we are a group of students from UC Irvine, taking the class CS175: Project in Artificial Intelligence. Well we've wondered why as CS majors who declared specialization in AI we were never required to take any classes about neural network, but here we are, at our final capstone project class finding out that we do not need knowledge about neural networks at all. All we need to know is reinforced learning in order to complete this class to graduate. Hooray!

Speaking of our project, by following the requirment and using Microsoft's [Malmo](https://github.com/microsoft/malmo) package, we're able to implement the game of minesweeper in Minecraft, where the board is transformed into a Minecraft map, and there're two layers of blocks: one layer of safety or potential bombs, and another layer of universal blocks for the agent to break. Once the agent breaks a surface block (like a tile in the original minesweeper game), it will see either a bomb or a block of different colors, substituting blocks with different numbers in the original game. Specific algorithms used are descried in [status.md](https://github.com/WenhanKong/Minesweepers/blob/master/docs/status.md), but the following articles/websited have offered us tremendous help during our project's making process:

- [Minesweeper Wiki](http://www.minesweeper.info/wiki/)
- [How to Beat Minesweeper](https://www.instructables.com/id/How-to-beat-Minesweeper/)
- [Solving Minesweeper](https://magnushoff.com/minesweeper/)
- [How cellular automaton plays Minesweeper](https://www.sciencedirect.com/science/article/pii/S0096300396001178?via%3Dihub)
- [Infinite versions of minesweeper are Turing complete](http://web.mat.bham.ac.uk/R.W.Kaye/minesw/infmsw.pdf)
- [Richard Kaye's Minesweeper Pages](http://web.mat.bham.ac.uk/R.W.Kaye/minesw/)

If you're interested in the minesweeper game, we highly suggest you look beyond our peojct and check our the above links also. Peace!

