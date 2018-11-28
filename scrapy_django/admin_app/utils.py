
import random
import hashlib

POOL = '1234567890qwertyuiopasdfghjklzxcvbnm!@#$%^&*()_+[]{};'

def getSalt():
    return ''.join(random.sample(POOL,6))

def hashCode(pwd,salt=None):
    h = hashlib.md5()
    if not salt:
        salt = getSalt()
    password = pwd + salt
    h.update(password.encode())
    return h.hexdigest()