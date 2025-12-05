import math
from functools import lru_cache
import time

def time_fn(name, fn):
    start = time.time()
    res = fn()
    end = time.time()
    print(f'function {name} took {end - start} seconds')
    return res
    
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

def sieve_brute_force(n):
    if n < 2:
        return []
    if n == 2:
        return [2]
    primes = [2]
    for i in range(3, n + 1, 2):
        if is_prime(i):
            primes.append(i)
    return primes

def sieve(n):
    primes = [True]*(n+1)
    primes[0] = False
    primes[1] = False
    sqrt_n = int(math.sqrt(n))
    for p in range(2, sqrt_n+1):
        if primes[p] == True:
            if not p*p <= n:
                break
            for i in range(p*p, n+1, p):
                primes[i] = False
    return [i for i,p in enumerate(primes) if p == True]

def segmented_sieve(n):
    sqrt_n = int(math.sqrt(n))
    # primes less than sqrt(n)
    primes = sieve(sqrt_n)
    # then all numbers form sqrt_n < k <= n 
    # are prime or have a factor p <= sqrt_n
    primes_in_segments = []
    # now mark off all that are multiples of p in primes
    for left in range(sqrt_n+1, n+1, sqrt_n):
        # need a range [left, left+sqrt_n) at most to [left, n]
        # the exclusion of left+sqrt_n is that the next segment 
        # will have it as its start
        right = min(left + sqrt_n - 1, n)
        # [left, right]
        segment = [True] * (right - left + 1)
        for p in primes:
            # find first multiple of p in range
            # a*p <= left
            start = (left // p) * p
            # when p doesn't divide left
            if start < left:
                start += p

            # cross out multiples of p in range
            for i in range(start-left, right-left + 1, p):
                segment[i] = False
        
        # the gaps are primes 
        primes_in_segments += [left+i for i,p in enumerate(segment) if p == True]
    
    return primes + primes_in_segments
            
        
    

def check_functions():
    for n in range(10, 10000, 300):
        assert(sieve(n) == sieve_brute_force(n))
    
    for n in range(10, 10000, 7):
        assert(segmented_sieve(n) == sieve(n))
    
    a = time_fn("segmented_sieve", lambda : segmented_sieve(100_000_000))
    b = time_fn("sieve", lambda : sieve(100_000_000))
    assert(a == b)
    assert(segmented_sieve(1_000_000) == sieve(1_000_000))

    
if __name__ == '__main__':
    # check_functions()
    a = time_fn("segmented_sieve", lambda : segmented_sieve(100_000_000))
    b = time_fn("sieve", lambda : sieve(100_000_000))
    assert(a == b)
    print(len(a))
    pass