# -*- coding:utf8 -*-

import random

class abstract_environnement(object):
    def __init__(self, taille_x, taille_y, condition_bords):
        self.taille_x, self.taille_y = taille_x, taille_y
        self.maille = -1
        self.nb_item = self.taille_x * self.taille_y
        tmp = {"dirichlet" : self.dirichlet,
               "neumann" : self.neumann,
               "torique" : self.torique}
        self.condition_bords = tmp.get(condition_bords)
        if not self.condition_bords :
            raise NotImplementedError(
                  "condition inconnue : {}".format(condition_bords))


    def init_maille(self):
        pass

    def __setitem__(self, xy, val):
        x, y = xy
        return x, y

    def dirichlet(self, x, y):
        if 0 <= y < self.taille_y and 0 <= x < self.taille_x :
            return x, y, None
        return x, y, 0

    def neumann(self, x, y):
        if y < 0 :
            pass
        if y >= self.taille_y:
            y = self.taille_y - 1
        if x < 0 :
            pass
        if x > self.taille_x:
            pass

    def torique(self, x, y):
        return x % self.taille_x, y % self.taille_y, None

    def __getitem__(self, xy):
        x, y = xy
        val = None
        return x, y, val

    def __str__(self):
        sep = '-----------------------------'
        res = '{}\ntaille : {}x{} -> {}\n'.format(sep,
                                                self.taille_x, self.taille_y,
                                                self.nb_item)
        return res


class list1d(abstract_environnement):
    def __init__(self, taille_x, taille_y, condition_bords):
        super(list1d, self).__init__(taille_x, taille_y, condition_bords)
        self.maille = [None for i in xrange(self.nb_item)]

    def init_maille(self, func_init):
        self.maille = [func_init() for i in self.maille]

    def __setitem__(self, xy, val):
        x, y = super(list1d, self).__setitem__(xy)
        self.maille[self.convert_coord(x, y)] = val

    def convert_coord(self, x, y):
        return self.taille_y * x + y

    def __getitem__(self, xy):
        x, y, val = super(list1d, self).__getitem__(xy)
        if val is None:
            return self.maille[self.convert_coord(x, y)]
        else:
            return val

    def __str__(self):
        res = super(list1d, self).__str__()
        res += 'max : {}, min : {}'.format(max(self.maille), min(self.maille))
        return res

if __name__ == '__main__':
    a = list1d(10, 10, "dirichlet")
    print a[2, 3]
    print(a)
