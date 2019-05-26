#! python3
# coding=utf-8

import random


class RandomUtils:

    @staticmethod
    def get_random_int(random_range=None):
        if random_range is None:
            ret = random.random()
        return ret
