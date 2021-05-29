class Coin():
    def __init__(self):
        self._public_key = 'pk'
        self._private_key = 'pk'
        self._value = 50

    @property
    def public_key(self):
        return self._public_key

    @property
    def value(self):
        return self._value
