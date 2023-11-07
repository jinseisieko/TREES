import random


def series_non_repeating_numbers(n, a0, a1, nested=False):
    lst = list(range(a0, a1 + 1))
    random.shuffle(lst)
    lst = lst[:n]

    if nested:
        new_lst = []
        for lst_x in lst:
            new_lst.append([lst_x])
        lst = new_lst

    return lst


class Tree:
    def __init__(self, map_size):
        super().__init__()
        self.map_size = map_size
        self.field = [[None for _ in range(1 + map_size * 2)] for _ in range(1 + map_size * 2)]

    def sprawl_in(self, cage, x, y, index):
        cage.set_coordinates(x, y)
        cage.map_ = self
        cage.index = index
        self.field[x][y] = cage

    def is_can_sprawl_in(self, x, y):
        if self.field[x][y] is None:
            return True
        else:
            return False

    def next(self):
        for elem in [a for b in self.field for a in b]:
            if elem is None:
                continue
            elem.sprawl()

    def set_seed(self, seed):
        if seed.count >= self.map_size:
            seed.count = self.map_size - 1

        self.field = [[None for _ in range(1 + self.map_size * 2)] for _ in range(1 + self.map_size * 2)]
        self.sprawl_in(seed, self.map_size, self.map_size, 0)

    def __str__(self):
        def func1(a0):
            return f"\033[0m{str(a0)}" if a0 is None else f"\033[32m{str(a0)}\033[0m" if a0.__class__.__name__ == "Leaves" else f"\033[3;31m{str(a0)}\033[0m"

        def func2(a0):
            return "\t".join(map(func1, a0))

        return "\n\n".join(map(func2, self.field))


class Cage:
    @staticmethod
    def generate_chromosome(chromosome_size):
        chromosome = []
        for _ in range(chromosome_size):
            line = series_non_repeating_numbers(4, 0, chromosome_size - 1, True)
            for i in range(4):
                line[i] += [random.randint(0, 1)]
            chromosome.append([random.randint(0, 1)] + [line])
        return chromosome

    def __init__(self, chromosome_size=None, x=None, y=None, count=None, map_=None, parent=None, chromosome=None):
        super().__init__()
        self.x = x
        self.y = y
        self.map_ = map_
        self.parent = parent
        self.chromosome_size = chromosome_size
        self.count = count

        self.chromosome = chromosome
        self.id = None
        self.is_sprawl = False
        self.index = None


        self.set_characteristics()

    def set_characteristics(self):
        if self.parent is None:
            if self.chromosome is None:
                self.chromosome = self.generate_chromosome(self.chromosome_size)
            self.id = random.randint(0, 1048576)
            self.index = 0
        else:
            parent = self.parent

            i = 1
            while parent.parent:
                parent = parent.parent
                i += 1

            self.chromosome_size = parent.chromosome_size
            self.chromosome = parent.chromosome
            self.map_ = parent.map_
            self.id = parent.id
            self.count = parent.count - i

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

    def sprawl(self):
        if self.is_sprawl:
            return
        self.is_sprawl = True

        if self.chromosome[self.index][0] == 1:
            index1 = 0
            index2 = 0
            poss1 = 0
            poss2 = 0
            for i, line in enumerate(self.chromosome[self.index][1]):
                if line[0] > index1:
                    index2 = index1
                    index1 = line[0]
                    poss2 = poss1
                    poss1 = i
                    continue
                if line[0] > index2:
                    index2 = line[0]
                    poss2 = i
        else:
            index1 = self.chromosome_size + 1
            index2 = self.chromosome_size + 1
            poss1 = 0
            poss2 = 0
            for i, line in enumerate(self.chromosome[self.index][1]):
                if line[0] < index1:
                    index2 = index1
                    index1 = line[0]
                    poss2 = poss1
                    poss1 = i
                    continue
                if line[0] < index2:
                    index2 = line[0]
                    poss2 = i

        if poss1 == 0:
            nex_coordinate1 = (self.x - 1, self.y)
        elif poss1 == 1:
            nex_coordinate1 = (self.x, self.y + 1)
        elif poss1 == 2:
            nex_coordinate1 = (self.x + 1, self.y)
        elif poss1 == 3:
            nex_coordinate1 = (self.x, self.y - 1)
        else:
            print("Error")
            return

        if poss2 == 0:
            nex_coordinate2 = (self.x - 1, self.y)
        elif poss2 == 1:
            nex_coordinate2 = (self.x, self.y + 1)
        elif poss2 == 2:
            nex_coordinate2 = (self.x + 1, self.y)
        elif poss2 == 3:
            nex_coordinate2 = (self.x, self.y - 1)
        else:
            print("Error")
            return

        if self.map_.is_can_sprawl_in(*nex_coordinate1):
            if self.chromosome[self.index][1][poss1][1] == 1:
                self.map_.sprawl_in(Branch(self), nex_coordinate1[0], nex_coordinate1[1], index1)
            else:
                self.map_.sprawl_in(Leaves(self), nex_coordinate1[0], nex_coordinate1[1], index1)
        if self.map_.is_can_sprawl_in(*nex_coordinate2):
            if self.chromosome[self.index][1][poss2][1] == 1:
                self.map_.sprawl_in(Branch(self), nex_coordinate2[0], nex_coordinate2[1], index2)
            else:
                self.map_.sprawl_in(Leaves(self), nex_coordinate2[0], nex_coordinate2[1], index2)

    def __str__(self):
        return f"{self.__class__.__name__}"
        # + "\n".join(list(map(str, self.chromosome))))


class Seed(Cage):
    def __init__(self, count, chromosome_size=4, map_=None, x=None, y=None, chromosome=None):
        super().__init__(chromosome_size, x, y, count, map_, None, chromosome=chromosome)


class Branch(Cage):
    def __init__(self, parent, x=None, y=None):
        super().__init__(None, x, y, None, None, parent)
        if self.count <= 0:
            self.is_sprawl = True


class Leaves(Branch):
    def __init__(self, parent, x=None, y=None):
        super().__init__(parent, x, y)
        self.is_sprawl = True


if __name__ == '__main__':
    m = Tree(9)
    s = Seed(8, 4, m)
    # s.chromosome = [[1, [[3, 1], [1, 0], [2, 0], [0, 0]]],
    #                 [1, [[1, 1], [0, 1], [2, 0], [3, 0]]],
    #                 [1, [[0, 0], [1, 0], [2, 1], [3, 1]]],
    #                 [1, [[3, 1], [2, 0], [1, 0], [0, 0]]]]

    m.sprawl_in(s, 9, 9, 0)
    for _ in range(8):
        m.next()
    print(m)
