# Primes and Divisibility

> **日本語で読む →** [Primes.md](../../ja/NumberTheory/Primes.md)

Corresponding Lean file: `LeanMathAtlas/NumberTheory/Primes.lean`

## Contents

### Examples of Primes and Basic Properties
| Theorem name | Description |
|--------|------|
| `two_prime`, `three_prime`, ... | 2, 3, 5, 7 are prime (automatically verified with `decide`) |
| `prime_ge_two` | Every prime is at least 2 |
| `prime_divisors` | The only divisors of a prime p are 1 and p |
| `prime_odd_or_two` | Every prime other than 2 is odd |

### Greatest Common Divisor (GCD)
| Theorem name | Description |
|--------|------|
| `my_gcd_dvd_left`, `my_gcd_dvd_right` | The gcd divides both arguments |
| `my_dvd_gcd` | Greatest among common divisors (gcd property) |
| `my_gcd_comm` | Commutativity of gcd |
| `my_gcd_zero_right` | gcd(a, 0) = a |
| `my_gcd_self` | gcd(a, a) = a |

### Coprimality
| Theorem name | Description |
|--------|------|
| `coprime_succ` | Consecutive integers are coprime (proof: the gcd divides 1) |
| `prime_coprime_of_not_dvd` | If p does not divide a, then gcd(p, a) = 1 |
| `coprime_dvd_of_dvd_mul` | Gauss's lemma: gcd(k,n)=1 and k\|mn ⟹ k\|m |

### Euclid's Theorem
| Theorem name | Description |
|--------|------|
| `exists_prime_ge` | For any n, there exists a prime ≥ n (infinitely many primes) |

## Learning Points

- The `decide` tactic automatically verifies propositions by finite computation. It can be used for primality testing.
- `Nat.Coprime a b` unfolds to the definition `Nat.gcd a b = 1`.
- The proof of `coprime_succ` uses the elementary idea that gcd(n, n+1) divides (n+1) − n = 1.
