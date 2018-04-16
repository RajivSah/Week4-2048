from Grid_3 import Grid
import math
from random import randint
from BaseAI_3 import BaseAI


class PlayerAI(BaseAI):

    def __init__(self):
        self.direction = -1
        self.weight = [[6, 5, 4, 3], [5, 4, 3, 2], [4, 3, 2, 1], [3, 2, 1, 0]]

    def possibleChild(self, grid):
        available_moves = grid.getAvailableMoves()
        children = {}
        for i in available_moves:
            child = grid.clone()
            child.move(i)
            children[i] = child

        return children

    def get4MaxTiles(self, grid):
        max_tiles = [0, 0, 0, 0]
        for x in range(4):
            for y in range(4):
                for i in max_tiles:
                    if i < grid.map[x][y]:
                        max_tiles[0] = grid.map[x][y]
                        break
                max_tiles.sort()

        return max_tiles

    def getNewTileValue(self):
        if randint(0, 1) == 0:
            return 2
        else:
            return 4

    def getPosition(self, grid, value):
        for x in range(4):
            for y in range(4):
                if value == grid.map[x][y]:
                    return [x, y]

    def crossBound(self, pos):
        return pos[0] < 0 or pos[0] >= 4 or pos[1] < 0 or pos[1] >= 4


    def heuristics(self, grid):
        # free cell heuristics
        free_cells = grid.getAvailableCells()
        free_cells_no = len(free_cells)

        # corner heuristics
        max_tile = grid.getMaxTile()
        max_tile_pos = self.getPosition(grid, max_tile)
        corner_heuristics = 0
        if max_tile_pos in [[0, 0], [0, 3], [3, 0], [3, 3]]:
            corner_heuristics = 10

        # Weight Matrix
        score = sum(grid.map[x][y]* self.weight[x][y] for x in range(4) for y in range(4))

        #clusters of equal valued tiles
        penalty = 0
        for x in range (4):
            for y in range(4):
                for zx in [x-1, x+1]:
                    if not self.crossBound([zx, y]):
                        penalty = penalty + abs(grid.map[x][y] - grid.map[zx][y] )
                for zy in [y-1, y+1]:
                    if not self.crossBound([x, zy]):
                        penalty = penalty + abs(grid.map[x][y] - grid.map[x][zy])

        print (free_cells_no, math.log2(score), 0.5*math.log2(penalty))
        return ( math.log2(score) - 0.5 * math.log2(penalty))

    def minimax(self, grid, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            return [self.heuristics(grid), -1]

        if maximizingPlayer:
            children = self.possibleChild(grid)
            if children == []:
                return [alpha, self.direction]
            for child in children:
                v = self.minimax(children[child], depth - 1, alpha, beta, False)
                if alpha < v[0]:
                    self.direction = child
                if v[0] == -math.inf:
                    self.direction = child
                alpha = max(alpha, v[0])
                if beta <= alpha:
                    break
            result = [alpha, self.direction]
            return result
        else:
            cells = grid.getAvailableCells()
            if cells == []:
                return None
            i = cells[randint(0, len(cells) - 1)]
            grid.map[i[0]][i[1]] = self.getNewTileValue()
            v = self.minimax(grid, depth - 1, alpha, beta, True)
            beta = min(beta, v[0])
            return [beta, v[1]]

    def getMove(self, grid):
        result = self.minimax(grid, 7, -math.inf, math.inf, True)
        return result[1]
