from __future__ import division
#import numpy as np
import random

def genFence(size,t):
    return '<DrawCuboid x1="0" y1="227" z1="0" x2="'+str(size+1)+'" y2="227" z2="'+str(size+1)+'" type="'+t+'"/>'

def genBlock(x,y,z,t):
    return '<DrawBlock x="'+str(x)+'" y="'+str(y)+'" z="'+str(z)+'" type="'+str(t)+'"/>'

def genBlockWithColor(x,y,z,t,c):
    return '<DrawBlock x="'+str(x)+'" y="'+str(y)+'" z="'+str(z)+'" type="'+str(t)+'" colour="'+str(c)+'"/>'

def genObservationFromGrid(size):
    return '<Grid name="board" absoluteCoords="1"> <min x="1" y="227" z="1"/> <max x="'+str(size)+'" y="228" z="'+str(size)+'10"/> </Grid>'

class Tile(object):
    def __init__(self):
        self.mine = False
        self.visible = False
        self.counter = 0
        self.marked_as_mine = False

class Minesweeper(object):

    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    win = False
    
    def __init__(self, size, num_mines):
        self.size = size
        self.num_mines = num_mines
        self.board = [[Tile() for n in range(size)] for n in range(size)]
        self.non_visible_counter = self.size * self.size
        self.end = False 

        for i in range(num_mines):
            while True:
                x = random.randint(0,size-1)
                y = random.randint(0,size-1)
                if self.board[x][y].mine == False:
                    self.board[x][y].mine = True
                    break
        for row in range(self.size):
            for col in range(self.size):
                currentTile = self.board[row][col]
                if currentTile.mine == False:
                    for (dx, dy) in self.directions:
                        if self.inbounds(row+dx, col+dy)==True and self.board[row+dx][col+dy].mine == True:
                            self.board[row][col].counter+=1

    def drawBoard(self):
        res = ''
        # -- different color maps to counter in Tile Class. -- #
        counter_color_dict = {1:'ORANGE', 2:'MAGENTA', 3:'LIGHT_BLUE', 4:'YELLOW', 5:'LIME', 6:'PINK', 7:'RED', 8:'BLACK'}
        
        # -- generate a diamond block fence with size of self.size * self.size -- #
        res+=genFence(self.size, "diamond_block")
        for x in range(self.size):
            for z in range(self.size):
                if self.board[x][z].mine == True:
                    res+=genBlock(x+1,227,z+1,"tnt")
                    res+="\n"
                else:
                    #tiles with no mines nearby are default wool
                    if self.board[x][z].counter == 0:
                        res+=genBlock(x+1,227,z+1,"wool")
                    else:
                        res+=genBlockWithColor(x+1, 227, z+1, "wool", counter_color_dict[self.board[x][z].counter])
                    res+="\n"
                # -- generate a glass cuboid as cover, not using genFence because layer starts at (1,1) -- #
                if not self.board[x][z].visible:
                    res+=genBlock(x+1, 228, z+1, 'stone')
                elif self.board[x][z].marked_as_mine:
                    res+=genBlock(x+1, 228, z+1, 'galss')
                else:
                    res+=genBlock(x+1, 228, z+1, 'air')
        return res

    def sweep(self, row, col):
        if(self.board[row][col].mine):
            print('This Tile Is A Mine! You Lost!')
            self.end = True
        else:
            self.search(row, col)

        self.checkWinCondition()

    def checkWinCondition(self):
        self.non_visible_counter = 0
        for row in self.board:
            for tile in row:
                if not tile.visible:
                    self.non_visible_counter+=1
        if self.non_visible_counter == self.num_mines:
            self.end = True
            self.win = True
            print('You Won! You have uncovered all non-mine blocks.')

    def search(self, row, col):
        #check if the coord is inbound
        if not self.inbounds(row, col):
            return
        #check if the tile is already visible or is it a mine
        tile = self.board[row][col]
        if tile.visible:
            return
        if tile.mine:
            return 
        #reveal a non mine non visible tile, stop if mines in adjacent tiles
        tile.visible = True
        if tile.counter > 0:
            return
        for (dx, dy) in self.directions:
            self.search(row+dx, col+dy)
        

    def inbounds(self, row, col):
        if 0<=row<self.size and 0<=col<self.size:
            return True
        else:
            return False

    def drawBoardAfterEnd(self):
        res = ''
        # -- different color maps to counter in Tile Class. -- #
        counter_color_dict = {1:'ORANGE', 2:'MAGENTA', 3:'LIGHT_BLUE', 4:'YELLOW', 5:'LIME', 6:'PINK', 7:'RED', 8:'BLACK'}
        
        # -- generate a diamond block fence with size of self.size * self.size -- #
        res+=genFence(self.size, "diamond_block")
        for z in range(self.size):
            for x in range(self.size):
                if self.board[z][x].mine == True:
                    res+=genBlock(x+1,227,z+1,"tnt")
                    res+="\n"
                else:
                    #tiles with no mines nearby are default wool
                    if self.board[z][x].counter == 0:
                        res+=genBlock(x+1,227,z+1,"wool")
                    else:
                        res+=genBlockWithColor(x+1, 227, z+1, "wool", counter_color_dict[self.board[z][x].counter])
                    res+="\n"
                # -- remove all cover -- #
                res+=genBlock(x+1, 228, z+1, 'air')
                
        return res

# -- For Debug -- #

    def printBoard(self):
        res = []
        for row in self.board:
            temp = []
            for tile in row:
                if tile.visible == True:
                    if tile.counter == 0:
                        temp.append(str(' '))
                    else:
                        temp.append(str(tile.counter))
                else:
                    temp.append('?')
            res.append(temp)
        for i in res:
            print(i)
    
    def printFullBoard(self):
        res = []
        for row in self.board:
            temp = []
            for tile in row:
                if tile.mine == True:
                    temp.append('*')
                else:
                    temp.append(str(tile.counter))
            res.append(temp)
        for i in res:
            print(i)