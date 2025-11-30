from functools import lru_cache
import math
from time import time

PRIMES = [2]

@lru_cache
def prime_factors(n : int) -> dict:
    f = {}
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            f[i] = f.get(i, 0) + 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

def is_prime(n):
    return sum(prime_factors(n).values()) == 1
    # if n <= 1:
    #     return False
    # else:
    #     is_prime = True  # Flag variable
    #     for i in range(2, int(n**0.5) + 1):
    #         if n % i == 0:
    #             is_prime = False
    #             break
    # return is_prime
    
def rl_prime(n):
    while not n == 0:
        # print(n)
        if not is_prime(n):
            return False
        n = n // 10  
    return True

def lr_prime(n, b):
    while not b == 0:
        print(n,b)
        if not is_prime(n):
            return False
        n = n % b
        b //= 10  
    return True

# print(rl_prime(3797))
# print(lr_prime(3797, 1000))
ends_with = {1, 2, 3, 5, 7}
print(is_prime(35))
d = 2
res = []
while True:

    s = 10**(d-1)
    new_ends_with = set()
    for digit in range(1, 9 + 1):
        p = digit * s
        for end in ends_with:
            q = p + end
            if not is_prime(q):
                continue
            
            if rl_prime(q) and lr_prime(q, s):
                res.append(q)   
                print("sol:", q, is_prime(q)) 
            if len(res) == 11:
                break
            new_ends_with.add(q)
    d += 1

    if len(new_ends_with) == 0:
        break
    if len(res) == 11:
        break
    ends_with = new_ends_with
    
    print(d, len(new_ends_with))
# print(ends_with)
print(res)
print(sum(res))