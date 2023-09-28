import string
import random 



def public_key_():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=40))

def private_key_():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=40))

def payment_ref():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=40))

def transactional_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=40))


