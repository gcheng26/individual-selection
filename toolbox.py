import numpy as np
from random import randrange

Gc = 0.018
Gs = 0.02
Cc = 0.1
Cs = 0.2
N = 4000
T = 1000
K = 0.1
Rs = 4
Rl = 50
t = 4

class Group:

    group_no = 0
    group_names = []
    members = []

    def __init__(self, genotype):
        self.type = genotype
        self.size = 4 if genotype == 0 else 40
        self.group_id = Group.group_no
        self.r_c, self.r_s = 0, 0
        self.prop, self.pool = [0, 0, 0, 0], [0, 0, 0, 0]
        Group.group_names.append(self.group_id)
        Group.group_no += 1

    def add_member(self, individual):
        self.members.append(individual)

    def get_proportions(self):
        for member in self.members:
            self.prop[member] += 1

    def calc_r(self):
        if self.type == 0:
            self.r_c = (self.prop[0] * Gc * Cc * Rs) / ((self.prop[0] * Gc * Cc) + (self.prop[1] * Gs * Cs))
            self.r_s = Rs - self.r_c

        elif self.type == 1:
            self.r_c = (self.prop[2] * Gc * Cc * Rl) / ((self.prop[2] * Gc * Cc) + (self.prop[3] * Gs * Cs))
            self.r_s = Rl - self.r_c

    def update_pop(self):
        for i in range(t):
            self.pool[0] = self.prop[0] + int(self.r_c/Cc) + K * self.prop[0]










class MigrantPool(Group):

    size = 0
    migrants = []