import string
import random


def create_password_grant():
    source = string.ascii_letters + string.digits
    return ''.join((random.choice(source) for i in range(8)))
