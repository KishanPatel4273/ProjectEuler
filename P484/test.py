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

def pi(x):
    return x / math.log(x)

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

def previous_prime(p):
    assert(not p == 2)
    if p == 3:
        return 2
    if p % 2 == 1:
        p -= 2
    while not is_prime(p):
        p -= 2
    return p

def next_prime(p):
    assert(p > 1)
    if p == 2:
        return 3
    if p % 2 == 0:
        p += 1
    else:
        p += 2
    while not is_prime(p):
        p += 2
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

def product(list : list[int]) -> int:
    res = 1
    for e in list:
        res *= e
    return res    

def p1():
    N = 5 * int(10 ** 15)
    p12_1 = 70710677
    p12_2 = 70710649
    P = p12_2
    prev = [p12_1]
    g = 2
    
    while product(prev) <= N:
        p = prev[-1]
        while not is_prime(p := p + 2):
            pass
        if len(prev) == g:
            P = prev.pop(0)
        prev.append(p)
    print(f'g={g} P={P} w/ {prev} *> {product(prev)},; {len(prev)} {product(prev) <= N}')


def find_meta_groups():
    N = 5 * int(10 ** 15)
    for g in range(13, 1 - 1, -1):
        start = int(N**(1/(g+1)))
        print(f'Stat for g = {g} is {start}')
        while not is_prime(start := start + 2):
            pass
        prev = [start]
        while product(prev) <= N:
            p = prev[-1]
            while not is_prime(p := p + 2):
                pass
            if len(prev) == g:
                prev.pop(0)
            prev.append(p)
        print(f'g={g} P={prev} *> {product(prev)}')

    
# find_meta_groups()
# exit()
# p1()

    
p12 = 70710707

N = 5 * int(10 ** 15)

# p_ = 2
# for i in range(3, int(math.sqrt(N))):
#     if is_prime(i):
#         if i**i <= N:
#             p_ = i
#             continue
#         print(p_, p_**p_ <= N, i, i**i <= N)
#         p_ = i
#         break

p_root_N = 70_710_649
p_root_N_1 = next_prime(p_root_N)
p_root_N_2 = next_prime(p_root_N_1)
print(f'    {p_root_N} * {p_root_N_1} <= N, so end of measure 2 group G(p)')
print(f'not {p_root_N_1} * {p_root_N_2} <= N, so end of measure 2 group G(p)')
assert(p_root_N**2 <= N)
assert(not p_root_N**3 <= N)
assert(p_root_N * p_root_N_1 <= N)
assert(not p_root_N_1 * p_root_N_2 <= N)

p3 = 70_957
p3_1 = next_prime(p3)
p3_2 = next_prime(p3_1)
p3_3 = next_prime(p3_2)
assert(p3 * p3_1 * p3_2 <= N)
assert(not p3 * p3_1 * p3_2 * p3_3 <= N)

assert(p3_2 * p3_3 <= N)
print(f'p3 = {p3} is start of measure 3, with range of q in ({p3}, {int((N/p3)**.5)}] to have q^2')

print(f'p = {2}, the range of q for q^2 is (2, {int((N/(2))**.5)}]')

primes_in_3p = 0
for n in range(70_957 + 1, 265_452 + 1):
    if is_prime(n):
        primes_in_3p += 1
print(f'p = {2}, the range of q for q^2 is (2, {int((N/(2))**.5)}] which has {primes_in_3p} primes in it')

print(pi( (N/(2)) ** .5 ))

