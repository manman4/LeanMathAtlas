import Mathlib.Tactic
import Mathlib.RingTheory.Ideal.Basic
import Mathlib.RingTheory.Ideal.Quotient.Basic
import Mathlib.RingTheory.Ideal.Quotient.Defs
import Mathlib.RingTheory.Ideal.Span
import Mathlib.RingTheory.Ideal.Maximal
import Mathlib.Data.ZMod.Basic
import Mathlib.RingTheory.ZMod

/-!
# Ring Theory: Rings, Ideals, and Quotient Rings

Working with `CommRing`, `Ideal`, quotient rings `R ⧸ I`, and the
prime/maximal ideal correspondence.

**Requires**: `CommRing`, `Ideal`, `Ideal.Quotient`, `ZMod`
**Tags**: Algebra, RingTheory
-/

variable {R : Type*} [CommRing R]

-- ============================================================
-- 1. 環の基本法則 (Ring Axioms)
-- ============================================================

-- 分配法則: a * (b + c) = a * b + a * c
theorem my_mul_add (a b c : R) : a * (b + c) = a * b + a * c := mul_add a b c
theorem my_add_mul (a b c : R) : (a + b) * c = a * c + b * c := add_mul a b c

-- 可換環: a * b = b * a
theorem my_mul_comm (a b : R) : a * b = b * a := mul_comm a b

-- 零乗法: a * 0 = 0, 0 * a = 0
theorem my_mul_zero (a : R) : a * 0 = 0 := mul_zero a
theorem my_zero_mul (a : R) : 0 * a = 0 := zero_mul a

-- 環では -1 * a = -a
theorem my_neg_one_mul (a : R) : -1 * a = -a := neg_one_mul a

-- 単位元: a * 1 = a
theorem my_mul_one (a : R) : a * 1 = a := mul_one a

-- ============================================================
-- 2. イデアル (Ideals)
-- ============================================================

-- イデアルは加法について閉じている
theorem my_ideal_add_mem (I : Ideal R) {a b : R} (ha : a ∈ I) (hb : b ∈ I) :
    a + b ∈ I :=
  I.add_mem ha hb

-- イデアルは左乗法について閉じている
theorem my_ideal_mul_mem_left (I : Ideal R) (r : R) {a : R} (ha : a ∈ I) :
    r * a ∈ I :=
  I.mul_mem_left r ha

-- イデアルは右乗法について閉じている（可換環では同じ）
theorem my_ideal_mul_mem_right (I : Ideal R) (r : R) {a : R} (ha : a ∈ I) :
    a * r ∈ I :=
  I.mul_mem_right r ha

-- 単項イデアル: a は (a) に属する
theorem my_mem_span_singleton_self (a : R) : a ∈ Ideal.span ({a} : Set R) :=
  Ideal.mem_span_singleton_self a

-- (1) = R（単位元が生成するイデアルは全体）
theorem my_span_one : (Ideal.span ({1} : Set R)) = ⊤ :=
  Ideal.span_singleton_one

-- (a) = R ↔ a は単元
theorem my_span_singleton_eq_top (a : R) :
    Ideal.span ({a} : Set R) = ⊤ ↔ IsUnit a :=
  Ideal.span_singleton_eq_top

-- 任意の真のイデアルは極大イデアルに含まれる
theorem my_exists_le_maximal (I : Ideal R) (hI : I ≠ ⊤) :
    ∃ M : Ideal R, M.IsMaximal ∧ I ≤ M :=
  Ideal.exists_le_maximal I hI

-- ============================================================
-- 3. 商環 (Quotient Rings)
-- ============================================================

-- 商環の射影: mk I は環準同型 R → R ⧸ I
-- mk I a = 0 ↔ a ∈ I
theorem my_quotient_eq_zero_iff (I : Ideal R) (a : R) :
    Ideal.Quotient.mk I a = 0 ↔ a ∈ I :=
  Ideal.Quotient.eq_zero_iff_mem

-- mk I a = mk I b ↔ a - b ∈ I（合同関係）
theorem my_quotient_mk_eq_iff (I : Ideal R) (a b : R) :
    Ideal.Quotient.mk I a = Ideal.Quotient.mk I b ↔ a - b ∈ I :=
  Ideal.Quotient.mk_eq_mk_iff_sub_mem a b

-- ============================================================
-- 4. 素イデアルと極大イデアルの対応
-- ============================================================

-- 素イデアル → R ⧸ I は整域
theorem my_isPrime_iff_isDomain (I : Ideal R) :
    I.IsPrime ↔ IsDomain (R ⧸ I) :=
  (Ideal.Quotient.isDomain_iff_prime I).symm

-- 極大イデアル → R ⧸ I は体
theorem my_isMaximal_iff_isField (I : Ideal R) :
    I.IsMaximal ↔ IsField (R ⧸ I) :=
  Ideal.Quotient.maximal_ideal_iff_isField_quotient I

-- 極大イデアルは素イデアル（体 ⊃ 整域）
theorem my_isMaximal_isPrime (I : Ideal R) (hM : I.IsMaximal) :
    I.IsPrime :=
  hM.isPrime

-- ============================================================
-- 5. 具体例 — ℤ の場合
-- ============================================================

-- 5ℤ は ℤ の素イデアル（5 が素数）
theorem span_five_isPrime : (Ideal.span ({(5 : ℤ)} : Set ℤ)).IsPrime := by
  rw [Ideal.span_singleton_prime (by norm_num)]
  exact Int.prime_iff_natAbs_prime.mpr (by norm_num)

-- ℤ → ZMod n の核 = nℤ
theorem ker_intCast_eq_span (n : ℕ) :
    RingHom.ker (Int.castRingHom (ZMod n)) = Ideal.span ({(n : ℤ)} : Set ℤ) :=
  ZMod.ker_intCastRingHom n

-- ZMod 5 は体（5 は素数）
instance : Fact (Nat.Prime 5) := ⟨by norm_num⟩

example : Field (ZMod 5) := inferInstance
example : IsDomain (ZMod 5) := inferInstance

-- ZMod 4 には零因子が存在（4 は素数でない）
-- 2 * 2 = 0 in ℤ/4ℤ, しかし 2 ≠ 0
example : (2 : ZMod 4) * 2 = 0 := by decide
example : (2 : ZMod 4) ≠ 0 := by decide
-- よって ZMod 4 は整域でなく、4ℤ は素イデアルでない

-- ZMod 6 での計算
example : (3 : ZMod 6) * 2 = 0 := by decide
example : (3 : ZMod 6) ≠ 0 := by decide
