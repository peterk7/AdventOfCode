import math

# Memoization cache for prime calculations
_prime_cache = []  # List of primes found so far, in order
_checked_up_to = 2  # We've verified all numbers in range [2, _checked_up_to)


def primesLowerThan(n):
    """Return all primes less than n, using cached results when available."""
    global _prime_cache, _checked_up_to

    if n <= 2:
        return []

    # Extend cache if needed
    if n > _checked_up_to:
        for candidate in range(_checked_up_to, n):
            if _isPrimeUsingCache(candidate):
                _prime_cache.append(candidate)
        _checked_up_to = n

    # Return primes less than n (binary search would be overkill for typical use)
    return _cachedPrimesLowerThan(n)


def _isPrimeUsingCache(n):
    """Check primality using cached primes (only checks up to √n)."""
    if n < 2:
        return False

    # Only need to check divisibility by primes up to √n
    upperLimit = int(math.isqrt(n)) + 1
    for p in _cachedPrimesLowerThan(upperLimit):
        if n % p == 0:
            return False
    return True


def _cachedPrimesLowerThan(n):
    global _prime_cache
    return [p for p in _prime_cache if p < n]
