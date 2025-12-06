from buildingGroups import sieve
from itertools import combinations
import math


def legendre(n):
    """Calculates the number of primes p such that sqrt(n) < p <= n according to Legendre's formula.
    Needs to be proved!"""

    primes = sieve(int(math.sqrt(n)))
    minus = True
    numberOfPrimesInProduct = 1
    sum = n
    while True:

        primesToIterateOverInThisSum = combinations(primes, numberOfPrimesInProduct)
        sumCopy = sum
        for p in primesToIterateOverInThisSum:

            product = 1
            for x in p:
                product *= x
            temp = n // product

            if minus:
                temp *= -1
            sum += temp
        if sum == sumCopy:
            return sum - 1
        numberOfPrimesInProduct += 1
        minus = not minus


if __name__ == "__main__":
    # This slows down pretty quickly once the argument goes from 10^5 to 10^6.
    # Improvements need to be made in breaking out once it is recognized that the sum
    # won't change (since the products are too big relative to n), and/or coming up with
    # a more intelligent way to iterate over the primes as opposed to generating the (n,k)
    # combinations each iteration.
    print(legendre(100000))
