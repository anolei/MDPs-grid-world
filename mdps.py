import copy
from time import time


class dot():
    def __init__(self, val, state, direct: int = 0):
        self.val = val
        self.state = state
        # 1 is fixed
        # 0 is blank
        self.direct = direct
        # direct:
        # 0: west,1: east, 2: north, 3:south


class Grid():
    def __init__(self, grid_width, gamma, noise, vals, reward: int = 0):
        self.width = grid_width
        self.gamma = gamma
        self.noise = noise
        self.reward = reward
        self.grid = [[] for i in range(grid_width)]
        self.new_grid = [[] for i in range(grid_width)]
        self.initial(vals)

    def initial(self, vals):

        for i in range(self.width):
            for j in range(self.width):
                if vals[i][j] is not None:
                    self.grid[i].append(dot(vals[i][j], 1))
                    self.new_grid[i].append(dot(vals[i][j], 1))
                else:
                    self.grid[i].append(dot(0, 0))
                    self.new_grid[i].append(dot(0, 0))

    def show(self):

        print("grid:")
        for row in self.grid:
            for val in row:
                print(val.val, end="\t\t")
            print()

    def showDirect(self):
        print("policy:")
        for row in self.grid:
            for dir in row:
                if  dir.val - round (dir.val) != 0:
                    if dir.direct == 0:
                        print("<-", end="\t\t")
                    if dir.direct == 1:
                        print("->", end="\t\t")
                    if dir.direct == 2:
                        print("up", end="\t\t")
                    if dir.direct == 3:
                        print("down", end="\t\t")
                else:
                    print(dir.val, end ="\t\t")
            print()

    def stopiteration(self) :
        for i in range(self.width):
            for j in range(self.width):
                if self.grid[i][j].val != self.new_grid[i][j].val:
                    return False
        return True

    # def is_equal_policy(self) :
    #     for i in range(self.width):
    #         for j in range(self.width):
    #             if self.grid[i][j].direct != self.new_grid[i][j].direct:
    #                 return False
    #     return True

    def get_value(self, x, y, direct, grid) -> float:
        transit = [
            [max(x - 1, 0), y],
            [min(x + 1, self.width - 1), y],
            [x, max(y - 1, 0)],
            [x, min(y + 1, self.width - 1)]
        ]
        value = 0
# for i in range (0,3):
#     value += self.noise[i] * (self.reward + self.gamma * self )

        if direct % 2 == 0:
            value += self.noise[0] * (self.reward + self.gamma * grid[transit[direct][1]][transit[direct][0]].val)
            value += self.noise[1] * (
                    self.reward + self.gamma * grid[transit[(direct + 2) % 4][1]][transit[(direct + 2) % 4][0]].val)
            value += self.noise[2] * (
                    self.reward + self.gamma * grid[transit[(direct + 3) % 4][1]][transit[(direct + 3) % 4][0]].val)
            value += self.noise[3] * (
                    self.reward + self.gamma * grid[transit[direct + 1][1]][transit[direct + 1][0]].val)
        else:
            value += self.noise[0] * (self.reward + self.gamma * grid[transit[direct][1]][transit[direct][0]].val)
            value += self.noise[1] * (
                    self.reward + self.gamma * grid[transit[(direct + 2) % 4][1]][transit[(direct + 2) % 4][0]].val)
            value += self.noise[2] * (
                    self.reward + self.gamma * grid[transit[(direct + 1) % 4][1]][transit[(direct + 1) % 4][0]].val)
            value += self.noise[3] * (
                    self.reward + self.gamma * grid[transit[direct - 1][1]][transit[direct - 1][0]].val)
        return round(value, 3)

    def update_max_value(self, x: int, y: int):
        max_direct = 0

        max_value = float("-inf")
        for direct in range(4):
            value = self.get_value(x, y, direct, self.grid)
            if max_value < value:
                max_value = value
                max_direct = direct

        self.new_grid[y][x].val = max_value
        self.new_grid[y][x].direct = max_direct



    def value_iteration(self):
        times = 0
        while True:
            times += 1
            for y in range(self.width):
                for x in range(self.width):
                    if not self.grid[y][x].state:
                        self.update_max_value(x, y)
            if self.stopiteration():
                break
            self.grid = copy.deepcopy(self.new_grid)

        self.show()
        print("iteration times: ", times)

    def update_policy(self, x: int, y: int):
        max_direct = 0
        max_value = float("-inf")
        for direct in range(4):
            value = self.get_value(x, y, direct, self.new_grid)
            if max_value < value:
                max_value = value
                max_direct = direct
        self.new_grid[y][x].direct = max_direct

    def policy_iteration(self):
        i = 0
        while True:
            i += 1
            for y in range(self.width):
                for x in range(self.width):
                    if not self.grid[y][x].state:
                        self.new_grid[y][x].val = self.get_value(x, y, self.grid[y][x].direct, self.grid)
            for y in range(self.width):
                for x in range(self.width):
                    if not self.new_grid[y][x].state:
                        self.update_policy(x, y)
            if self.stopiteration():
                break
            self.grid = copy.deepcopy(self.new_grid)
        self.show()
        self.showDirect()
        print("iteration times: ", i)


if __name__ == '__main__':
    grid = [
        [None, None, None, 1, None, None, None],
        [None, None, None, -1, None, 1, None],
        [- 1, None, None, -1, None, 4, None],
        [None, 1, None, -1, None, 1, None],
        [None, 100, None, -100, None, 3, None],
        [None, 2, None, -1, None, 3, None],
        [0, None, None, -1, None, 1, None]
    ]
    noise = [0.8, 0.1, 0.1, 0]
    gamma = 0.9
    # policy iteration
    print("gamma:", gamma)
    print("noise:", noise)

    testGrid = Grid(len(grid), gamma, noise, grid)
    start_time = time()

    testGrid.update_max_value(0, 0)

    testGrid.show()
    testGrid.policy_iteration()
    print("policy iteration runtime: %.2f s" % (time() - start_time))

 #   value iteration
    start_time = time()
    testGrid = Grid(7, 0.9, noise, grid)
    testGrid.update_max_value(2, 4)


    testGrid.show()
    testGrid.value_iteration()
    print("value iteration runtime: %.2f s" % (time() - start_time))

