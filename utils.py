import pickle
import hashlib


def serialize(block):
    return pickle.dumps(block)

def deserialize(data):
    return pickle.loads(data)

def hash(content):
    return content

def sign(content, key):
    obj = {
        'content': content,
        'key': key
    }
    return obj

def encode(str, code='utf-8'):
    return str.encode(code)

def decode(bytes, code='utf-8'):
    return bytes.decode(code)

def sum256_hex(*args):
    m = hashlib.sha256()
    for arg in args:
        m.update(arg)
    return m.hexdigest()
