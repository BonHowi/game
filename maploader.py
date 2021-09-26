from environment import Wall


class MapLoader:
    def __init__(self, game):
        self.game = game
        self.map = []
        self.block_w = 0
        self.block_h = 0
        self.load_map()
        self.add_walls()

    def load_map(self):
        with open('maps/map1.txt') as file:
            self.map = [list(line)[:-1] for line in file.readlines()]
        self.map.reverse()
        for idx, element in enumerate(self.map):
            self.map[idx].reverse()
        self.block_w = int(self.game.SIZE[0] / len(self.map)) + 1
        self.block_h = int(self.game.SIZE[1] / len(self.map)) + 1

    def add_walls(self):
        for idx, element in enumerate(self.map):
            for i, char in enumerate(element):
                if char == "#":
                    pos_x = int(self.game.SIZE[0] - self.game.SIZE[0] / len(element) * i) - self.block_w
                    pos_y = int(self.game.SIZE[1] - self.game.SIZE[1] / len(self.map) * idx) - self.block_h
                    self.game.wall_list.append(Wall(self.game, self.block_w, self.block_h, pos_x, pos_y,
                                                    (10, 19, 10),
                                                    self.game.all_wall))
