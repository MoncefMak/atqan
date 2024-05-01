import random
import string


def generate_otp():
    characters = string.digits + string.ascii_letters
    otp = ''.join(random.choices(characters, k=6))
    return otp
