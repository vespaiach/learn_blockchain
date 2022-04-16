from hashlib import sha256


def is_valid_hash(hash_str):
    return len(hash_str) == 64 and hash_str[0:2] == '00'


def gen_hash(transaction_str, nonce):
    return sha256((transaction_str + str(nonce)).encode()).hexdigest()


def find_valid_hash(transaction_str):
    nonce = 0
    hashing = gen_hash(transaction_str, nonce)

    while is_valid_hash(hashing) == False:
        nonce += 1
        hashing = gen_hash(transaction_str, nonce)

    return nonce, hashing
