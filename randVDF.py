"""
Simple implementation of VDF

"""

import time

class RandVDF():

    def __init__(self):
        self.ek = None
        self.vk = None

    def setup(self):
        pass

    def reset(self):
        pass

    def eval(self, input, s, slot):
        output = self._start(input, int_state)
        # TODO
        for i in range(s):
            output = self._iterate(output, ek, int_state)
            slot += 1

        output = self._prove(output, ek, int_state)
        return (input, output, proof, rand_iter, slot)

    def verify(self, input, rand_source, proof, rand_iter):
        return True


    def _start(self, input, int_state):
        return input

    def _iterate(self, input, int_state):
        start_time = time.time()
        pass

    def _prove(self, input, ek, int_state):
        pass