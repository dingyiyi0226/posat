"""
Block structure

    header:

    content:
    {
        'tx':
        'coin':
        'input':
        'rand_source':
        'proof':
        'rand_iter':
        'slot':
        'state':  hash of the parent block
    }

    sign:

"""


import utils

from coin import Coin


default_content = {
    'tx': [],
    'coin': Coin(),
    'input': 0,
    'rand_source': 0,
    'proof': 'genesis',
    'rand_iter': 0,
    'slot': 0,
    'state': ''
}

class Block():

    def __init__(self, header='', content=default_content, sign='', level=0):
        self._header = header
        self._content = content
        self._sign = sign
        self._level = level
        self._hash = self._get_hash()

    def __repr__(self):
        return (
            "Block:\n"
            f"  header: {self._header}\n"
            f"  content-tx: {self.tx}\n"
            f"  content-coin: {self.coin}\n"
            f"  content-input: {self.input}\n"
            f"  content-rand_source: {self.rand_source}\n"
            f"  content-proof: {self.proof}\n"
            f"  content-rand_iter: {self.rand_iter}\n"
            f"  content-slot: {self.slot}\n"
            f"  content-state: {self.parent_blk}\n"
            f"  sign: {self._sign}\n"
            f"  level: {self.level}\n"
            f"  hash: {self.hash}\n"
        )

    @property
    def tx(self):
        return self._content['tx']

    @property
    def coin(self):
        return self._content['coin']

    @property
    def input(self):
        return self._content['input']

    @property
    def rand_source(self):
        return self._content['rand_source']

    @property
    def proof(self):
        return self._content['proof']

    @property
    def rand_iter(self):
        return self._content['rand_iter']

    @property
    def slot(self):
        return self._content['slot']

    @property
    def parent_blk(self):
        return self._content['state']

    @property
    def level(self):
        return self._level

    @property
    def hash(self):
        return self._hash

    def is_unspent(self):
        return self._content['coin'].value > 0

    def _get_hash(self):
        block_string = [
            str(self.coin),
            str(self.input),
            str(self.proof),
            str(self.rand_iter),
            str(self.slot)
        ]
        encode_str = utils.encode(''.join(block_string))
        hash_str = utils.sum256_hex(encode_str)
        return hash_str


if __name__ == '__main__':

    header = 'header'
    content = {
        'tx': ['asd', 'as'],
        'coin': '',
        'input': 'input',
        'rand_source': 'rs',
        'proof': 'pf',
        'rand_iter': 'ri',
        'slot': 3,
        'state': 'aaas'
    }
    sign = 'sign'

    block = Block(header, content, sign)
    print(block)
