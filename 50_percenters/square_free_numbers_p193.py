import math
import time

def square_free_numbers(n):
    sqrt_n = int(math.sqrt(n))
    # primes index | value
    #          p   | 1
    #  square free | number of distinct primes
    #         else | 0
    primes = [-1]*(sqrt_n+1)
    primes[0] = 0
    primes[1] = 1

    for p in range(2, sqrt_n+1):
        if primes[p] == -1:
            # p is prime
            p2 = p*p
            for i in range(p, sqrt_n+1, p):
                # non square free number
                if primes[i] == 0:
                    continue
                # count distinct primes
                if primes[i] == -1:
                    primes[i] = 1
                else:
                    primes[i] += 1
                # mark of non square free numbers
                if i % p2 == 0:
                    primes[i] = 0
    square_free = n
    for d,m in enumerate(primes):
        if d < 2:
            continue
        if m == 0:
            continue
        # excluding all numbers that have factor d*d
        # the sign is for inclusion exclusion to add back
        square_free += (1 if m%2==0 else -1) * (n // (d*d))
    return square_free     

assert(square_free_numbers(int(1E7)) == 6_079_291)

def solve():
    N = int(2**50)
    start = time.time()
    sfn = square_free_numbers(N)
    end = time.time()
    print(f'Q({N}) = {sfn}     in {end-start} [s]')
    
if __name__ == '__main__':
   solve()