import pickle
import hashlib


def serialize(block):
    return pickle.dumps(block)

def deserialize(data):
    return pickle.loads(data)

def sign(content, key):
    sign_str = ''.join([str(i) for i in content.values()])
    return sum256_hex(encode(sign_str))

def encode(str, code='utf-8'):
    return str.encode(code)

def decode(bytes, code='utf-8'):
    return bytes.decode(code)

def sum256_hex(*args):
    m = hashlib.sha256()
    for arg in args:
        m.update(arg)
    return m.hexdigest()

def hash(output, slot):
    return output + slot

def threshold(s):
    return s*0.1
