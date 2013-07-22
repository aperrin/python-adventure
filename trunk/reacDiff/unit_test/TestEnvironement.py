#import sys
#sys.path.append('.')
from ..src import environement


class TestEnvironement():
    def __init__(self):
        self.taille_x = 10
        self.taille_y = 10
        condition_bords = "dirichlet"
        self.env = environement.list1d(self.taille_x, self.taille_y, condition_bords)
        self.env.init_maille(lambda : 1)

    def test_taille(self):
        """
        """
        assert(self.taille_x == self.env.taille_x)
        assert(self.taille_y == self.env.taille_y)

    def test_init(self):
        """
        """
        for x in xrange(self.taille_x):
            for y in xrange(self.taille_y) :
                assert(self.env[x, y] == 1)

    def test_dirichlet(self):
        pass

if __name__ == '__main__':
    print 'plop'
