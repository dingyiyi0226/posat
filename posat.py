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

class Posat():

    def __init__(self):

        self._block_bucket = Bucket(db_file, block_bucket)
        self._tx_bucket = Bucket(db_file, tx_bucket)

        try:
            self.parent_blk = self._block_bucket.get(latest)
        except KeyError:
            genesis = Block()
            self.send_block(genesis)
            self.parent_blk = genesis.hash

        self.un_cnf_tx = self._tx_bucket.get()

        self.rand_source = None
        self.slot = None
        self.participate = False

    def receive_msg(self, msg):
        pass

    def receive_tx(self):
        txs = self._tx_bucket.get()
        print(txs)
        for tx in txs:
            if not self._is_valid_tx(tx):
                continue
            self.un_cnf_tx.append(tx)

    def _is_valid_tx(self, tx):
        return type(tx) == str

    def receive_block(self):
        block = utils.deserialize(self._block_bucket.get(latest))

        if not self._is_valid_block(block):
            return
        if self.parent_blk.level < block.level:
            self._change_main_chain(block)
            if block.level % c == 0:
                self.rand_source = block.rand_source
            if self.participate:
                randVDF.reset()
            if block.level % c == 0 and not self.participate:
                self.slot = block.slot
                self.participate = True

    def _change_main_chain(self, block):
        self._parent_blk = block.hash

    def _is_valid_block(self, block):
        if not block.is_unspent():
            return False

        parent_blk = utils.deserialize(self._block_bucket.get(block.parent_blk))
        if parent_blk.slot >= block.slot:
            return False

        # TODO
        s = 5

        return randVDF.verify(block.input, block.rand_source, block.proof, block.rand_iter)


    def pos_leader_election(self, coin):

        sign_key = coin.public_key
        # stake = coin.stake(search_chain_up(self.parent_blk))
        # s = update_threshold(stake)
        stake = coin.value
        s = stake * 0.5

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
        return Block(header, content, utils.sign(content, sign_key), self.parent_blk.level+1)

    def send_block(self, block):
        self._block_bucket.put(block.hash, utils.serialize(block))
        self._block_bucket.put(latest, block.hash)
        self._block_bucket.commit()
        self.remove_txs(block.tx)

    def remove_txs(self, txs):
        for tx in txs:
            self._tx_bucket.delete(tx)
        self._tx_bucket.commit()

    def send_tx(self, tx):
        self._tx_bucket.put(tx, tx)
        self._tx_bucket.commit()


if __name__ == '__main__':
    client = Posat()
    coin = Coin()
    # block = client.pos_leader_election(coin)
    # client.send_tx('hellso')
    client.receive_tx()
    # print(block)
