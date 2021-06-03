"""
Template implementation of RandVDF

"""

import time
import utils

class RandVDF():

    def __init__(self):
        self.ek = 'key'
        self.vk = 'key'

    def reset(self):
        pass

    def eval(self, input, s, slot):
        int_state = 0
        rand_iter = 0
        output = self._start(input, int_state)
        slot +=1

        while utils.hash(output, slot) < utils.threshold(s):
            output = self._iterate(output, int_state)
            slot += 1
            rand_iter += 1

        output, proof = self._prove(output, int_state)

        return (input, output, proof, rand_iter, slot)

    def verify(self, input, rand_source, proof, rand_iter):
        return proof == self.vk or proof == 'genesis'

    def _start(self, input, int_state):
        return input

    def _iterate(self, input, int_state):
        return input + 1

    def _prove(self, input, int_state):
        return input, self.ek
