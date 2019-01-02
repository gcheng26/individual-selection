import numpy as np
from random import randrange

G_coop = 0.018
G_selfish = 0.02
C_coop = 0.1
C_selfish = 0.2
N = 4000
T = 1000
K = 0.1
Res_s = 4
Res_l = 50
t = 4


class SmallGroup:

    group_no = 0
    group_names = []

    def __init__(self, genotype):
        self.type = genotype
        self.group_id = SmallGroup.group_no
        self.share = [0, 0]
        self.prop, self.pool = [0, 0], [0, 0]
        self.members = []
        SmallGroup.group_names.append(self.group_id)
        SmallGroup.group_no += 1

    def add_member(self, individual):
        self.members.append(individual)

    def get_proportions(self):
        for member in self.members:
            self.prop[member] += 1

    def calc_r(self):
        if self.type == 'small':
            self.share[0] = (self.prop[0] * G_coop * C_coop * Res_s) / \
                            ((self.prop[0] * G_coop * C_coop) + (self.prop[1] * G_selfish * C_selfish))
            self.share[1] = Res_s - self.share[0]

        else:
            raise Exception('Type error! - Should be Small but is {}' .format(self.type))

    def update_pop(self):
        # net increase (births - deaths) cooperative
        self.calc_r()
        self.pool[0] = int(self.share[0] / C_coop) - int(K * self.prop[0])
        # initial + births + deaths of cooperative
        self.prop[0] = self.prop[0] + self.pool[0]
        # net increase (births - deaths) selfish
        self.pool[1] += int(self.share[1] / C_selfish) - int(K * self.prop[1])
        # initial + births + deaths of selfish
        self.prop[1] = self.prop[1] + self.pool[1]

    def get_pool(self):
        return self.pool

    def pop_pop(self):
        self.members = self.members[0:4]


class LargeGroup:

    group_no = 0
    group_names = []

    def __init__(self, genotype):
        self.type = genotype
        self.group_id = LargeGroup.group_no
        self.share = [0, 0]
        self.prop, self.pool = [0, 0], [0, 0]
        self.members = []
        LargeGroup.group_names.append(self.group_id)
        LargeGroup.group_no += 1

    def add_member(self, individual):
        self.members.append(individual)

    def init_proportions(self):
        for member in self.members:
            self.prop[member-2] += 1

    def calc_r(self):
        if self.type == 'large':
            self.share[0] = (self.prop[0] * G_coop * C_coop * Res_l) / \
                            ((self.prop[0] * G_coop * C_coop) + (self.prop[1] * G_selfish * C_selfish))
            self.share[1] = Res_s - self.share[0]

        else:
            raise Exception('Type error! - Should be Large but is {}' .format(self.type))

    def update_pop(self):
        # net increase (births - deaths) cooperative
        self.calc_r()
        self.pool[0] = int(self.share[0] / C_coop) - int(K * self.prop[0])
        # initial + births + deaths of cooperative
        self.prop[0] = self.prop[0] + self.pool[0]
        # net increase (births - deaths) selfish
        self.pool[1] = int(self.share[1] / C_selfish) - int(K * self.prop[1])
        # initial + births + deaths of selfish
        self.prop[1] = self.prop[1] + self.pool[1]

    def get_pool(self):
        return self.pool

    def get_members(self):
        return self.members

    def pop_pop(self):
        self.prop= [0, 0]
        self.members = self.members[0:40]
        

class MigrantPool(SmallGroup):
    size = 0
    migrants = []


