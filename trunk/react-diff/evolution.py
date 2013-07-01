# -*- coding:utf8 -*-

import random

from environement import list1d


class abstract_evolution(object):
    def __init__(self, taille_x, taille_y, condition_bords):
        self.terrain = list1d(taille_x, taille_y, condition_bords)
        self.terrain.init_maille(self.init_terrain())

    def init_terrain(self):
        def plop():
            return random.randint(0, 1)
        return plop

    def run():
        pass


class evolution_convolution_list(abstract_evolution):
    def __init__(self, taille_x, taille_y, condition_bords):
        super(evolution_convolution_list, self).__init__(taille_x, taille_y, condition_bords)
        self.laplacian = [[0, 1, 0],
                          [1, -4, 1],
                          [0, 1, 0]]




a = abstract_evolution(100, 100, "dirichlet")
print a.terrain
