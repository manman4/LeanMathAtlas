import Mathlib.Tactic
import Mathlib.Topology.Basic
import Mathlib.Topology.Compactness.Compact
import Mathlib.Topology.Connected.Basic
import Mathlib.Topology.Order.Compact
import Mathlib.Topology.Order.IntermediateValue

/-!
# Topology: Open Sets, Compactness, and Connectedness

Working with topological spaces, continuous maps, compact sets, and connected sets.

**Requires**: `TopologicalSpace`, `IsCompact`, `IsConnected`, `Continuous`
**Tags**: Topology
-/

variable {X Y : Type*} [TopologicalSpace X] [TopologicalSpace Y]

-- ============================================================
-- 1. 開集合と閉集合 (Open and Closed Sets)
-- ============================================================

-- 全体集合と空集合は開集合
theorem my_isOpen_univ : IsOpen (Set.univ : Set X) := isOpen_univ
theorem my_isOpen_empty : IsOpen (∅ : Set X) := isOpen_empty

-- 開集合の有限交差は開集合
theorem my_isOpen_inter {s t : Set X} (hs : IsOpen s) (ht : IsOpen t) :
    IsOpen (s ∩ t) :=
  hs.inter ht

-- 開集合の任意合併は開集合
theorem my_isOpen_iUnion {ι : Type*} {f : ι → Set X} (h : ∀ i, IsOpen (f i)) :
    IsOpen (⋃ i, f i) :=
  isOpen_iUnion h

-- 開集合と閉集合の双対性: s が開 ↔ sᶜ が閉
theorem my_isClosed_compl_iff {s : Set X} : IsClosed sᶜ ↔ IsOpen s :=
  isClosed_compl_iff

-- 閉集合の有限合併は閉集合
theorem my_isClosed_union {s t : Set X} (hs : IsClosed s) (ht : IsClosed t) :
    IsClosed (s ∪ t) :=
  hs.union ht

-- 閉集合の任意交差は閉集合
theorem my_isClosed_iInter {ι : Type*} {f : ι → Set X} (h : ∀ i, IsClosed (f i)) :
    IsClosed (⋂ i, f i) :=
  isClosed_iInter h

-- 「開集合は有限交差で、閉集合は有限合併で閉じる」
-- 逆は一般に成立しない（無限のとき）
-- 例: ⋂ n, (-1/n, 1/n) = {0} は閉集合（開ではない）

-- ============================================================
-- 2. 連続写像 (Continuous Maps)
-- ============================================================

-- 連続写像の特徴付け: 開集合の逆像が開
theorem my_isOpen_preimage {f : X → Y} (hf : Continuous f) {s : Set Y} (hs : IsOpen s) :
    IsOpen (f ⁻¹' s) :=
  hs.preimage hf

-- 連続写像の合成は連続
theorem my_continuous_comp {Z : Type*} [TopologicalSpace Z]
    {f : X → Y} {g : Y → Z} (hf : Continuous f) (hg : Continuous g) :
    Continuous (g ∘ f) :=
  hg.comp hf

-- 恒等写像は連続
theorem my_continuous_id : Continuous (id : X → X) := continuous_id

-- 定数写像は連続
theorem my_continuous_const {y : Y} : Continuous (fun _ : X => y) := continuous_const

-- ============================================================
-- 3. コンパクト集合 (Compact Sets)
-- ============================================================

-- コンパクト集合の有限被覆性: 任意の開被覆は有限部分被覆を持つ
theorem my_isCompact_elim_finite_subcover {s : Set X} (hs : IsCompact s)
    {ι : Type*} (U : ι → Set X) (hU : ∀ i, IsOpen (U i)) (hcover : s ⊆ ⋃ i, U i) :
    ∃ t : Finset ι, s ⊆ ⋃ i ∈ t, U i :=
  hs.elim_finite_subcover U hU hcover

-- コンパクト集合と閉集合の交差はコンパクト
theorem my_isCompact_inter_right {s t : Set X} (hs : IsCompact s) (ht : IsClosed t) :
    IsCompact (s ∩ t) :=
  hs.inter_right ht

-- コンパクト集合の閉部分集合はコンパクト
theorem my_isCompact_of_isClosed_subset {s t : Set X}
    (hs : IsCompact s) (ht : IsClosed t) (h : t ⊆ s) : IsCompact t :=
  hs.of_isClosed_subset ht h

-- 連続写像によるコンパクト集合の像はコンパクト
theorem my_isCompact_image {s : Set X} {f : X → Y}
    (hs : IsCompact s) (hf : Continuous f) : IsCompact (f '' s) :=
  hs.image hf

-- ============================================================
-- 4. 連結集合 (Connected Sets)
-- ============================================================

-- 単元集合は連結
theorem my_isConnected_singleton {x : X} : IsConnected ({x} : Set X) :=
  isConnected_singleton

-- 連結集合の合併（共通点を持つ）は連結
theorem my_isConnected_union {s t : Set X} (H : (s ∩ t).Nonempty)
    (hs : IsConnected s) (ht : IsConnected t) : IsConnected (s ∪ t) :=
  hs.union H ht

-- 連続写像による連結集合の像は連結
theorem my_isConnected_image {s : Set X} {f : X → Y}
    (hs : IsConnected s) (hf : Continuous f) : IsConnected (f '' s) :=
  hs.image f hf.continuousOn

-- 連結空間全体も連結
theorem my_isConnected_univ [ConnectedSpace X] : IsConnected (Set.univ : Set X) :=
  isConnected_univ

-- ============================================================
-- 5. 具体例 — ℝ の場合
-- ============================================================

-- ℝ の閉区間はコンパクト（ハイネ・ボレルの定理の特殊形）
example : IsCompact (Set.Icc (0 : ℝ) 1) := isCompact_Icc

example (a b : ℝ) : IsCompact (Set.Icc a b) := isCompact_Icc

-- ℝ の閉区間は連結（中間値の定理の背景）
example : IsConnected (Set.Icc (0 : ℝ) 1) := isConnected_Icc (by norm_num)

example (a b : ℝ) (h : a ≤ b) : IsConnected (Set.Icc a b) := isConnected_Icc h

-- ℝ は連結空間
example : ConnectedSpace ℝ := inferInstance

-- ℝ 全体は連結
example : IsConnected (Set.univ : Set ℝ) := isConnected_univ

-- コンパクト × 閉の具体例: [0,1] ∩ [0.5, 2] = [0.5, 1] はコンパクト
example : IsCompact (Set.Icc (0 : ℝ) 1 ∩ Set.Icc (1/2) 2) :=
  isCompact_Icc.inter_right isClosed_Icc

-- 連続写像の像: sin : [0, π] → [-1, 1] はコンパクトかつ連結な値域に対応
example : IsCompact ((fun x : ℝ => Real.sin x) '' Set.Icc 0 Real.pi) :=
  isCompact_Icc.image Real.continuous_sin

example : IsConnected ((fun x : ℝ => Real.sin x) '' Set.Icc 0 Real.pi) :=
  (isConnected_Icc (by positivity)).image _ Real.continuous_sin.continuousOn
