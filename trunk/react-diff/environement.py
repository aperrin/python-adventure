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

    def check_bord(self, x, y):
        res_y, res_x = True, True
        if x > self.taille_x or x < 0 :
            res_x = False
        if y > self.taille_y or y < 0 :
            res_y = False
        return res_x, res_y

    def neumann(self, x, y):


    def torique(self, x, y):
        return x % self.taille_x, y % self.taille_y

    def __getitem__(self, xy):
        x, y = xy

        return x, y

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

    def dirichlet(self, x, y):
        res = super(list1d, self).dirichlet(x, y)
        if res == 0 :
            return 0
        else :
            return self.maille[self.convert_coord(x, y)]

    def __getitem__(self, xy):
        x, y = super(list1d, self).__getitem__(xy)
        return self.maille[self.convert_coord(x, y)]

    def __str__(self):
        res = super(list1d, self).__str__()
        res += 'max : {}, min : {}'.format(max(self.maille), min(self.maille))
        return res

if __name__ == '__main__':
    a = list1d(10, 10, "dirichlet")
    print a[2, 3]
    print(a)
