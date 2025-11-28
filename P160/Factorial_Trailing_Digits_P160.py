from functools import lru_cache
import math
from time import time

@lru_cache
def is_whole_number(n : int) -> bool:
    if isinstance(n, int):
        return True
    elif isinstance(n, float):
        return n.is_integer()
    else:
        return False

@lru_cache
def is_natural_number(n) -> bool:
    return not n == 0 and is_whole_number(n)

@lru_cache
def is_multiple_of_five(n : int) -> bool:
    return is_whole_number(n) and (n % 10 in {0, 5})

# number of trailing zeros for n!
def number_of_trailing_zeros_of_factorial(n : int) -> int:
    assert(is_natural_number(n))
    n = int(n)
    R = range(1, int(math.log(n) / math.log(5)) + 1)
    z = lambda i : n // 5**i
    return sum(map(z,  R))
assert(number_of_trailing_zeros_of_factorial(9) == 1)
assert(number_of_trailing_zeros_of_factorial(10) == 2)
assert(number_of_trailing_zeros_of_factorial(20) == 4)

PRIMES = [2]

@lru_cache
def prime_factors(n : int) -> dict:
    assert(is_natural_number(n))
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
    q = last_prime
    while q*q <= n:
        if n % q == 0:
            PRIMES.append(q)
        while n % q == 0:
            n //= q
            f[q] = f.get(q, 0) + 1
        q += 1
    if n > 1:
        PRIMES.append(n)
        f[n] = f.get(n, 0) + 1
    return f
assert(prime_factors(2**2 * 5**33 * 7) == {2:2, 5:33, 7:1})

@lru_cache
def factors_of_five(n):
    if n == 0:
        return 0
    p = 0
    while n % 5 == 0:
        n //= 5
        p += 1
    return p

# computes a^n mod b 
# implements Right-to-left binary method
# [https://en.wikipedia.org/wiki/Modular_exponentiation#Right-to-left_binary_method]
@lru_cache
def mod_pow(a : int, n : int, b : int) -> int:
    assert(is_natural_number(a))
    assert(is_natural_number(b))
    assert(is_whole_number(n) and 0 <= n)
    if b == 1:
        return 0
    # (b-1) * (b-1) should not overflow
    product = 1
    a = a % b
    while 0 < n:
        if n % 2 == 1:
            product = (product * a) % b
        n = n >> 1
        a = (a * a) % b
    return product

def isValid_b(b : int) -> bool:
    return math.log10(b) % 1 == 0 and b > 1

def isValid_N(N : int) -> bool:
    return math.log10(N) % 1 == 0 and N > 1

def isValid_problem(N : int, b: int) -> bool:
    return isValid_N(N) and isValid_b(b) and b <= N

def isValid_sequence(r : int, v : int) -> bool:
    return r % 1 == 0 and is_natural_number(v) and 0 < v

def drop_fives(n : int) -> int:
    if n == 0:
        return n
    while n % 5 == 0:
        n //= 5
    return n
assert(drop_fives(5**23 * 7) == 7)

def first_multiple_of_five(r : int, v : int) -> int | None:            
    assert(is_natural_number(r))
    assert(is_natural_number(v))
    for d in range(10):
       if is_multiple_of_five((d*r + v) % 10):
           return d + 1
    return None

# series a_i = (i - 1) * r + v
# calculates the the product of (a_1 ... a_n) mod b
def product_of_sequence(r : int, v : int, b : int, n : int) -> int:
    assert(isValid_sequence(r, v))
    assert(is_natural_number(b))
    assert(is_natural_number(n))
    # period of sequence mod b
    t = b // math.gcd(r, b)
    pt, pr = 1, 1
    for i in range(1, min(t, n) + 1):
        a_i = (i - 1) * r + v
        pt *= a_i % b
        pt %= b
        if i == n % t:
            pr = pt
    product = mod_pow(pt, n//min(n, t), b)
    if not n < t:
        product * pr
    return product % b

# series a_i = (i - 1) * r + v
# calculates the the product of (a_1 ... a_n) / 5^p mod b
# where p is the number of factors in the product
def product_of_sequence_drop_five(r : int, v : int, b : int, n : int) -> int:
    assert(isValid_sequence(r, v))
    assert(is_natural_number(b))
    assert(is_natural_number(n))
    assert(is_multiple_of_five(b))
    # remove trivial factors of 5 in the series
    pr = factors_of_five(r)
    pv = factors_of_five(v)
    min_factors_of_five = min(pr, pv)
    reduce_sequence_by = 5**min_factors_of_five
    r = r // reduce_sequence_by
    v = v // reduce_sequence_by
    assert(not is_multiple_of_five(math.gcd(r, v)))

    if pv < pr:
        return product_of_sequence(r, v, b, n)
    
    # period of the sequence
    t = b // math.gcd(r, b)

    # check if series has a any more multiple of 5's
    offset = first_multiple_of_five(r, v)
    assert(offset <= 5)
    # ignore the a_i|5
    pt, pr = 1, 1
    for i in range(1, min(t, n) + 1):
        if offset is not None and is_multiple_of_five(i - offset):
            continue
        a_i = (i - 1) * r + v
        assert(not is_multiple_of_five(a_i))
        pt *= a_i % b
        pt %= b
        if i == n % t:
            pr = pt
    ignore_ever_fifth = mod_pow(pt, n//min(n, t), b)
    if not n < t:
        ignore_ever_fifth = (ignore_ever_fifth * pr) % b 
        
    # get product of a_i that where skipped
    p5s = 1
    if offset is not None:
        for i in range(offset, n + 1, 5):
            a_i = drop_fives((i - 1) * r + v)
            p5s *= a_i % b
            p5s %= b
    return (ignore_ever_fifth * p5s) % b

# solve problem (N, b)             
def solve(N : int, b : int):
    s = time()
    assert(is_natural_number(N))
    assert(is_natural_number(b))
    assert(isValid_problem(N, b))
    N, b = int(N), int(b)
    
    z = number_of_trailing_zeros_of_factorial(N)
    l = N // b
    Z = math.ceil(z / l)
    R = Z*l - z
    assert(Z <= 4 * b/10)
    print(f'({N}, {b}) ::<>:: lambda = {l}; z(N!) = {z}; Z = {Z} R = {R}')

    product = 1
    for v in range(1, b + 1):
        if v % 5 == 0:
            # pass
            product *= product_of_sequence_drop_five(b, v, b, l)
        elif v % 2 == 0 and 0 < Z:
            product *= product_of_sequence(b//2, v//2, b, l)
            Z -= 1
        else:
            product *= product_of_sequence(b, v, b, l)

        assert(not is_multiple_of_five(product))
        product %= b
    
    product *= mod_pow(2, R, b)
    product %= b
    e = time()
    print(f'({N}, {b}) = {product} \t took {e-s} [s]')

# solve(1_000, 1_000)
solve(1_000_000_000_000, 1E5)