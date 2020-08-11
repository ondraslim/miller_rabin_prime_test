from random import randrange


def is_prime_miller_rabin(n, k=128):
    """ Test if a number is prime using Miller Rabin algorithm.
        -> find a nontrivial square roots of 1 mod n
        - no Carmichael numbers
        - complexity: O(k * log(n))
        Args:
            n -- int -- the number to test
            k -- int -- the number of tests to do
        return True if n is prime
    """

    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    s, r = find_miller_rabin_r_s(n)

    for _ in range(k):
        if not miller_rabin_rand_test(n, s, r):
            return False
    return True


def find_miller_rabin_r_s(n):
    """ Find Miller-Rabin r, s coefficients satisfying:
         (n - 1) = r * ( 2 ** s), where r is odd
        Args:
            n -- int -- the number to test
        return s, r miller rabin coefficients
    """

    s = 0
    r = n - 1

    while r & 1 == 0:
        s += 1
        r //= 2
    return s, r


def miller_rabin_rand_test(n, s, r):
    """ Do one iteration of Miller-Rabin prime test:
        1) pick random A in range [1, n - 1]
        2) test:
            a) a**r != 1 (mod n) && a**((2**j) * r) != -1 (mod n)   for all j in range [0, s - 1]
                -> N is not a prime, A is a strong witness to compositeness for N
            b) a**r = 1 (mod n) || a**((2**j)* r) = -1 (mod n)      for some j in range [0, s - 1]
                -> N is not a prime, N is a strong pseudo-prime to the base A, A is strong liar to primality for N
        Args:
            n -- int -- the number to test
            s, r -- int, int -- the number to test, Miller Rabin coefficients satisfying:
                                (n - 1) = r * ( 2 ** s), where r is odd
        return s, r miller rabin coefficients
    """

    a = randrange(2, n - 1)
    x = pow(a, r, n)
    if x != 1 and x != n - 1:
        j = 1
        while j < s and x != n - 1:
            x = pow(x, 2, n)
            if x == 1:
                return False
            j += 1
        if x != n - 1:
            return False
    return True


def do_basic_tests():
    """ Run basic primality tests on Miller-Rabin algorithm implementation
        return True if tests successful
    """
    basic_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 53, 101, 131]
    basic_composites = [4, 6, 8, 9, 10, 16, 85, 94, 124, 133]

    for _ in range(10):
        for prime in basic_primes:
            if not is_prime_miller_rabin(prime):
                print("Miller-Rabin algorithm implementation failed to detect %d as a prime" % prime)
                return False

        for composite in basic_composites:
            if is_prime_miller_rabin(composite):
                print("Miller-Rabin algorithm implementation failed to detect %d as a composite" % composite)
                return False

    return True


if __name__ == '__main__':
    if do_basic_tests():
        print("Miller-Rabin probability algorithm basic tests successful")

    belphegors_prime = 1_000_000_000_000_066_600_000_000_000_001
    print("Number %s is prime? %s" % (belphegors_prime, is_prime_miller_rabin(belphegors_prime)))


