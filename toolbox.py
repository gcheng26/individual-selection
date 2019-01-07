import numpy as np
import matplotlib.pyplot as plt
from random import randrange

G_coop = 0.018
G_selfish = 0.02
C_coop = 0.1
C_selfish = 0.2
N = 4000
T = 150
K = 0.1
Res_s = 4
Res_l = 50
t = 4


class SmallGroup:

    group_no = 0
    group_names = []

    def __init__(self):
        self.type = 'small'
        self.group_id = SmallGroup.group_no
        self.prop, self.share, self.initial_seed = [0, 0], [0, 0], [0, 0]
        self.members = []
        SmallGroup.group_names.append('s' + str(self.group_id))
        SmallGroup.group_no += 1

    def add_member(self, individual):
        self.members = individual

    def get_proportions(self):
        for member in self.members:
            self.prop[member] += 1
            self.initial_seed[member] += 1

    def calc_r(self):
        if self.type == 'small':
            self.share[0] = (self.prop[0] * G_coop * C_coop * Res_s) / \
                            ((self.prop[0] * G_coop * C_coop) + (self.prop[1] * G_selfish * C_selfish))
            self.share[1] = Res_s - self.share[0]

        else:
            raise Exception('Type error! - Should be Small but is {}' .format(self.type))

    def update_pop(self):
        for i in range(t):
            self.calc_r()
            # initial + births + deaths of cooperative
            self.prop[0] = self.prop[0] + int(self.share[0] / C_coop) - int(K * self.prop[0])
            # initial + births - deaths of selfish
            self.prop[1] = self.prop[1] + int(self.share[1] / C_selfish) - int(K * self.prop[1])

    def get_progeny(self):
        return np.subtract(self.prop, self.initial_seed)

    def reset(self):
        self.prop, self.share, self.initial_seed = [0, 0], [0, 0], [0, 0]
        self.members = []

    def small_seq(self):
        self.get_proportions()
        self.update_pop()
        batch = self.get_progeny()
        self.reset()
        return batch


class LargeGroup:

    group_no = 0
    group_names = []

    def __init__(self):
        self.type = 'large'
        self.group_id = LargeGroup.group_no
        self.prop, self.initial_seed, self.share = [0, 0], [0, 0], [0, 0]
        self.members = []
        LargeGroup.group_names.append('l' + str(self.group_id))
        LargeGroup.group_no += 1

    def add_member(self, individual):
        self.members = individual

    def get_proportions(self):
        for member in self.members:
            self.prop[member-2] += 1
            self.initial_seed[member-2] += 1

    def calc_r(self):
        if self.type == 'large':
            self.share[0] = (self.prop[0] * G_coop * C_coop * Res_l) / \
                            ((self.prop[0] * G_coop * C_coop) + (self.prop[1] * G_selfish * C_selfish))
            self.share[1] = Res_l - self.share[0]

        else:
            raise Exception('Type error! - Should be Large but is {}' .format(self.type))

    def update_pop(self):
        for i in range(t):
            self.calc_r()
            # initial + births + deaths of cooperative
            self.prop[0] = self.prop[0] + int(self.share[0] / C_coop) - int(K * self.prop[0])
            # initial + births - deaths of selfish
            self.prop[1] = self.prop[1] + int(self.share[1] / C_selfish) - int(K * self.prop[1])

    def get_progeny(self):
        # print('prop')
        # print(self.prop)
        # print('seed')
        # print(self.initial_seed)
        return np.subtract(self.prop, self.initial_seed)

    def reset(self):
        self.prop, self.share, self.initial_seed = [0, 0], [0, 0], [0, 0]
        self.members = []

    def large_seq(self):
        self.get_proportions()
        self.update_pop()
        batch = self.get_progeny()
        self.reset()
        return batch


class MigrantPool(SmallGroup, LargeGroup):
    size = 0

    def __init__(self):
        self.prop = [0, 0, 0, 0]
        self.migrants, self.small_groups, self.large_groups = [], [], []
        self.total, self.temp_pool = 0, 0

    def first(self):
        for i in range(N):
            self.migrants.append(i % 4)

        print(self.migrants)

    def census(self):
        for member in self.migrants:
            self.prop[member] += 1

    def collect(self):
        self.prop = [0, 0, 0, 0]
        for small in self.small_groups:
            self.prop[0:2] = np.add(self.prop[0:2], small.small_seq())
        for large in self.large_groups:
            self.prop[2:4] = np.add(self.prop[2:4], large.large_seq())

    def rescale(self):
        self.total = sum(self.prop)
        for i in range(len(self.prop)):
            self.prop[i] = int((self.prop[i] * N) / self.total)

    def fill(self):
        self.migrants = []
        for j in range(len(self.prop)):
            for i in range(self.prop[j]):
                self.migrants.append(j)

    def assign(self):
        self.small_groups, self.large_groups = [], []
        for i in range(int((self.prop[0] + self.prop[1]) / 4)):
            self.small_groups.append(SmallGroup())
            self.small_groups[i].add_member(self.get_small_batch())
            # print(MigrantPool.small_groups[i].group_id)
            # self.small_groups[i].get_mem()
            # self.small_groups[i].get_proportions()

        for i in range(int((self.prop[2] + self.prop[3]) / 40)):
            self.large_groups.append(LargeGroup())
            self.large_groups[i].add_member(self.get_large_batch())
            # print(MigrantPool.large_groups[i].group_id)
            # self.large_groups[i].get_mem()
            # self.large_groups[i].get_proportions()

    def get_small_batch(self):
        small_batch = []
        while len(small_batch) != 4:
            idx = randrange(0, len(self.migrants))
            i = self.migrants[idx]
            if i <= 1:
                small_batch.append(self.migrants.pop(idx))
            else:
                pass

        return small_batch

    def get_large_batch(self):
        large_batch = []
        while len(large_batch) != 40:
            idx = randrange(0, len(self.migrants))
            i = self.migrants[idx]
            if i > 1:
                large_batch.append(self.migrants.pop(idx))
            else:
                pass
        return large_batch

    def clean(self):
        self.prop = [0, 0, 0, 0]
        self.migrants = []
        self.total = 0
        self.temp_pool = 0
        MigrantPool.size = 0
        MigrantPool.small_groups = []
        MigrantPool.large_groups = []


def start_seq():
    prop_arr = []
    gen = [0]
    migrant_pool = MigrantPool()
    migrant_pool.first()
    migrant_pool.census()
    prop_arr.append(migrant_pool.prop)
    for i in range(T):
        print('iteration no' + str(i))
        migrant_pool.assign()
        migrant_pool.collect()
        migrant_pool.rescale()
        print(migrant_pool.prop)
        prop_arr.append(migrant_pool.prop)
        gen.append(i+1)
        migrant_pool.fill()

    s_c = [i[0] for i in prop_arr]
    s_s = [i[1] for i in prop_arr]
    l_c = [i[2] for i in prop_arr]
    l_s = [i[3] for i in prop_arr]
    plt.plot(gen, s_c, '.', label='small + cooperative')
    plt.plot(gen, s_s, '-.', label='small + selfish')
    plt.plot(gen, l_c, ':', label='large + cooperative ')
    plt.plot(gen, l_s, '-', label='large + selfish')
    plt.xlabel('Generations')
    plt.ylabel('Frequecy')
    plt.legend()
    plt.show()



