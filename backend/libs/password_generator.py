import random

CHARS = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def password_generator(length):
    password = ''

    for _ in range(length):
        password += random.choice(CHARS)

    return password
