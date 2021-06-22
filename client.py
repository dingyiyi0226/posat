import utils
from randVDF import RandVDF
from db import Bucket
from block import Block
from coin import Coin

randVDF = RandVDF()
c = 1

latest = 'l'
db_file = 'blockchain.db'
block_bucket = 'blocks'
tx_bucket = 'txs'

class Client():

    def __init__(self):

        self._block_bucket = Bucket(db_file, block_bucket)
        self._tx_bucket = Bucket(db_file, tx_bucket)

        try:
            self.parent_blk = self._block_bucket.get(latest)
        except KeyError:
            genesis = Block()
            print('Genesis', genesis)
            self.send_block(genesis)
            self.parent_blk = genesis.hash

        self.un_cnf_tx = self._tx_bucket.get()

        self.rand_source = 0
        self.slot = 0
        self.participate = False

    def receive_msg(self, msg):
        pass

    def receive_tx(self):
        self._tx_bucket.refresh()
        txs = self._tx_bucket.get()
        if txs:
            print(txs)
            for tx in txs:
                if not self._is_valid_tx(tx):
                    continue
                self.un_cnf_tx.append(tx)
        else:
            print('No txs')
            self.un_cnf_tx.clear()

    def _is_valid_tx(self, tx):
        return type(tx) == str

    def receive_block(self):
        self._block_bucket.refresh()

        self.receive_tx()

        block_hash = self._block_bucket.get(latest)
        block = utils.deserialize(self._block_bucket.get(block_hash))
        print('block', block)

        if not self._is_valid_block(block):
            print('is not valid block')
            return

        parent_blk = utils.deserialize(self._block_bucket.get(self.parent_blk))
        # print('parent_blk', parent_blk)
        if parent_blk.level < block.level:
            self._change_main_chain(block)
            if block.level % c == 0:
                self.rand_source = block.rand_source
            if self.participate:
                randVDF.reset()
            if block.level % c == 0 and not self.participate:
                self.slot = block.slot
                self.participate = True

    def _change_main_chain(self, block):
        print('change main chain')
        self.parent_blk = block.hash

    def _is_valid_block(self, block):
        if not block.is_unspent():
            print('is_unspent')
            return False

        if block.parent_blk != '':
            parent_blk = utils.deserialize(self._block_bucket.get(block.parent_blk))
            if parent_blk.slot > block.slot:
                print('parent slot error')
                return False

            s = parent_blk.coin.value
            if utils.hash(block.rand_source, block.slot) < utils.threshold(s):
                print('hash error')
                return False

        return randVDF.verify(block.input, block.rand_source, block.proof, block.rand_iter)


    def pos_leader_election(self, coin):

        sign_key = coin.public_key
        stake = coin.value
        s = stake

        input = self.rand_source
        input, output, proof, rand_iter, slot = randVDF.eval(input, s, self.slot)
        self.rand_source = output
        state = self.parent_blk
        content = {
            'tx': self.un_cnf_tx,
            'coin': coin,
            'input': input,
            'rand_source': self.rand_source,
            'proof': proof,
            'rand_iter': rand_iter,
            'slot': slot,
            'state': state
        }
        header = 'header'
        self.un_cnf_tx = []

        parent_blk = utils.deserialize(self._block_bucket.get(self.parent_blk))
        return Block(header, content, utils.sign(content, sign_key), parent_blk.level+1)

    def send_block(self, block):
        self._block_bucket.put(block.hash, utils.serialize(block))
        self._block_bucket.put(latest, block.hash)
        self._block_bucket.commit()
        self.remove_txs(list(block.tx))

    def remove_txs(self, txs):
        for tx in txs:
            self._tx_bucket.delete(tx)
        self._tx_bucket.commit()

    def send_tx(self, tx):
        self._tx_bucket.put(tx, tx)
        self._tx_bucket.commit()

    def print_all_block(self):
        print('Blockchain:')

        blockchain = []
        tip = self.parent_blk
        while tip != '':
            block = utils.deserialize(self._block_bucket.get(tip))
            blockchain.append(block)
            tip = block.parent_blk

        for block in blockchain[::-1]:
            print(block)


if __name__ == '__main__':
    client = Client()
    coin = Coin()

    client.send_tx('ell')
    client.send_tx('el')
    client.receive_tx()
    block = client.pos_leader_election(coin)
    print(block)

    client.send_block(block)
    client.receive_tx()
    client.receive_block()

    client.print_all_block()
