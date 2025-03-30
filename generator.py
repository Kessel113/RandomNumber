from system_entropy import get_hardware_seed
import hashlib
from datetime import datetime
from bernstein import djb2

# def generate(base, seed, beg, end, count):
#     base = base.encode() if isinstance(base, str) else base
#     seed = seed.encode() if isinstance(seed, str) else seed

#     hw_seed = str(get_hardware_seed()).encode()
#     rand = hashlib.sha3_512(base + hashlib.sha3_512(seed + hw_seed).digest()).hexdigest()

#     rounds = 3
#     while rounds != 0:
#         hw_seed = str(get_hardware_seed()).encode()
#         rand += hashlib.sha3_512(base + hashlib.sha3_512(seed + hw_seed).digest()).hexdigest()
#         rounds -= 1
#     rand = int(rand, 16)
#     bit_len = (rand % (2048 - 128 + 1)) + 128
#     rand = rand & ((1 << bit_len) - 1)
#     rand = rand % (end - beg + 1) + beg
#     from datetime import datetime

#     current_time = datetime.now().strftime("%H:%M:%S")

#     print(f"\n!!! Random number #{count}(session) has been generated ({current_time})!!!\n")    
#     return rand

def generate(base, seed, beg, end, count):
    base = base.encode() if isinstance(base, str) else base
    seed = str(seed).encode() if not isinstance(seed, bytes) else seed
    hw_seed = str(get_hardware_seed()).encode()

    # base^seed => bernstein cate 64/4 B / dim max = nr pe 2 B
    base = hashlib.sha3_512(base).digest()
    seed_aux = hashlib.sha3_512(seed).digest()

    base = bytes(a ^ b for a, b in zip(base, seed_aux))
    base = djb2(base, end)

    base = str(base).encode() if not isinstance(base, bytes) else base


    rand = int.from_bytes(hashlib.sha3_512(base + hashlib.sha3_512(seed + hw_seed).digest()).digest(), 'big')
    
    for _ in range(3):  # 3 more rounds
        hw_seed = str(get_hardware_seed()).encode()
        rand ^= int.from_bytes(hashlib.sha3_512(rand.to_bytes(64, "big", signed=False) + hashlib.sha3_512(seed + hw_seed).digest()).digest(), 'big')

    rand %= (end - beg + 1) + beg
    print(f"\n!!! Random number #{count}(session) generated ({datetime.now().strftime('%H:%M:%S')})!!!\n")
    return rand