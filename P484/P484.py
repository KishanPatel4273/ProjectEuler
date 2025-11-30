import math
from functools import lru_cache
from random import randrange
import heapq


MAX_NUMBER_OF_PRIMES = 1E2
PRIMES = [2]
heapq.heapify(PRIMES)

@lru_cache
def prime_factors(n : int) -> dict:
    global PRIMES
    n = int(n)
    f : dict[int][int] = {}
    
    last_prime = None
    for p in PRIMES:
        while n % p == 0:
            n //= p
            f[p] = f.get(p, 0) + 1
        last_prime = p
        if n < p*p:
            break
    assert(last_prime is not None)
    q = 2
    while q*q <= n:
        if n % q == 0 and len(PRIMES) < MAX_NUMBER_OF_PRIMES:
            heapq.heappush(PRIMES, q)
        while n % q == 0:
            n //= q
            f[q] = f.get(q, 0) + 1
        q += 1
    if n > 1:
        PRIMES.append(n)
        f[n] = f.get(n, 0) + 1

@lru_cache   
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def number_of_primes_in_factorization_less_than_N(N):
    assert(not N == 1)
    product = 2
    p = 3
    i = 1
    while (next := product * p) <= N:
        product = next
        i += 1
        q = p + 2
        while not is_prime(q):
            q += 2
        p = q
    return i

# print(number_of_primes_in_factorization_less_than_N(N))
# f = {}
# for i in range(1, int(N) + 1):
#     pf = prime_factors(i)
#     s = len(pf.keys())
#     f[s] = f.get(s, 0) + 1
# print(f)
# print([v/N for v in f.values()])

def largest_prime_less_than(p):
    assert(not p == 2)
    if p == 3:
        return 2
    if p % 2 == 1:
        p -= 2
    while not is_prime(p):
        p -= 2
    return p
    

def p12():
    N = 5 * int(10 ** 15)
    print(5 * math.sqrt(2))
    p = int(5 * math.sqrt(2) * 10**7) + 1
    print(p)
    assert(p % 2 == 1)
    print(p, p*p <= N)
    while not is_prime(p := p + 2):
            pass
    while p*p <= N:
        while not is_prime(p := p + 2):
            pass
    print(p)
    
# p12()
print()
N = 5 * int(10 ** 15)
p1 = 70710707
p2 = 70710709
print(f'N = {N}')
print(70710709**2 <= N)
print(70710707**2 <= N)
print(70710677**2 <= N)

p12 = 70710707
print(N / math.log(N))
print(p12 / math.log(p12))
print(138319418975671 - 3912265 + 1 )
# print(largest_prime_less_than(p1))