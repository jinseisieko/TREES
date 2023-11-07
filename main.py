from PyQt5 import QtWidgets
from PyQt5.Qt import *

from tree import *

MAIN_WINDOW_SIZE = [1800, 900]
SIZE_PAINT = 900


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(*MAIN_WINDOW_SIZE)
        self.setWindowTitle("Tree")
        self.trees_map_size = 100
        self.count_trees = 1
        self.chromosome_size_seeds = 5
        self.trees = [Tree(map_size=self.trees_map_size)]
        self.set_seed_for_trees(self.generate_seeds())

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.timeout.connect(self.next_for_trees)
        self.timer.start(50)

        self.button = QPushButton(self)
        self.button.resize(80, 30)
        self.button.move(SIZE_PAINT+10, 0)
        self.button.clicked.connect(self.click_button)

    def click_button(self):
        self.trees = [Tree(map_size=self.trees_map_size)]
        self.set_seed_for_trees(self.generate_seeds())



    def set_seed_for_trees(self, seeds):
        for tree, seed in zip(self.trees, seeds):
            tree.set_seed(seed)

    def next_for_trees(self):
        for tree in self.trees:
            tree.next()

    def generate_seeds(self):
        seeds = []
        for _ in range(self.count_trees):
            seeds.append(Seed(count=self.trees_map_size, chromosome_size=self.chromosome_size_seeds))
        return seeds

    def get_new_seeds(self, chromosomes):
        seeds = []
        for chromosome in chromosomes:
            seeds.append(Seed(self.count_trees, self.chromosome_size_seeds, chromosome=chromosome))

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_tree(qp, self.trees[0], 0, 0, SIZE_PAINT)
        qp.end()

    def draw_tree(self, qp, tree, x, y, s1):
        rect = [s1 // len(tree.field), s1 // len(tree.field[0])]
        a = y
        for line in tree.field:
            b = x
            for el in line:
                if str(el.__class__.__name__) in ("Seed", "Branch"):
                    qp.setBrush(QColor(200, 100, 100))
                elif str(el.__class__.__name__) == "Leaves":
                    qp.setBrush(QColor(0, 255, 0))
                else:
                    qp.setBrush(QColor(255, 255, 255))
                qp.drawRect(b, a, rect[0], rect[1])
                b += rect[1]
            a += rect[0]


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
