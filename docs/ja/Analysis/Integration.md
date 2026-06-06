# 積分論: 区間積分と微積分の基本定理

> **Read in English →** [Integration.md](../../en/Analysis/Integration.md)

対応する Lean ファイル: `LeanMathAtlas/Analysis/Integration.lean`

## 内容

### 区間積分の基本性質

| 定理名 | 内容 |
|--------|------|
| `my_integral_const` | 定数関数の積分: ∫[a,b] c dx = (b-a) * c |
| `my_integral_symm` | 区間の向き: ∫[b,a] f = -∫[a,b] f |
| `my_integral_add` | 加法性: ∫(f+g) = ∫f + ∫g |
| `my_integral_sub` | 減法性: ∫(f-g) = ∫f - ∫g |
| `my_integral_smul` | スカラー倍: ∫ c•f = c • ∫f |
| `my_integral_add_adjacent` | 区間分割: ∫[a,b] + ∫[b,c] = ∫[a,c] |

### 積分可能性

| 定理名 | 内容 |
|--------|------|
| `my_continuous_intervalIntegrable` | 連続関数は区間積分可能 |

### 微積分の基本定理

| 定理名 | 内容 |
|--------|------|
| `my_ftc2` | 第2部: F' = f ならば ∫[a,b] f = F(b) - F(a) |
| `my_ftc1` | 第1部: d/dx ∫[a,x] f(t) dt = f(x) |

### 具体例

| 式 | 値 |
|----|----|
| ∫[0,1] x dx | 1/2 |
| ∫[0,1] x² dx | 1/3 |
| ∫[0,π] sin x dx | 2 |
| ∫[0,1] eˣ dx | e - 1 |

## 学習ポイント

- **区間積分の表記**: `∫ x in a..b, f x` は `intervalIntegral` で定義される区間 [a,b] 上の積分。
  Lean では測度論（`MeasureTheory`）の上に構築されている。

- **`IntervalIntegrable`**: 積分の加法性・減法性などの定理には `IntervalIntegrable f volume a b`
  （f が [a,b] 上で可積分であること）が必要。連続関数は常に可積分（`Continuous.intervalIntegrable`）。

- **FTC 第2部の使い方**:
  ```lean
  intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint
  -- hderiv : ∀ x ∈ Set.uIcc a b, HasDerivAt F (f x) x
  -- hint   : IntervalIntegrable f volume a b
  ```

- **原始関数の求め方**:
  ```
  f(x) = x     → F(x) = x²/2    (HasDerivAt を (hasDerivAt_pow 2 x).div_const 2 で構成)
  f(x) = x²    → F(x) = x³/3
  f(x) = sin x → F(x) = -cos x  (HasDerivAt を (Real.hasDerivAt_cos x).neg で構成)
  f(x) = eˣ   → F(x) = eˣ      (Real.hasDerivAt_exp x を直接使用)
  ```

- **FTC 第1部の使い方**:
  ```lean
  Continuous.deriv_integral f hf a b
  -- : deriv (fun u => ∫ x in a..u, f x) b = f b
  ```

- **スカラー積 `•` と実数乗**: ℝ では `c • x = c * x`（`smul_eq_mul`）。
  `integral_const` の結果は `(b - a) • c` という形なので、必要に応じて `smul_eq_mul` を使う。

## 計算例

```lean
-- ∫[0,π] sin x dx = 2
-- (-cos x)' = sin x (HasDerivAt.neg)
-- -cos π - (-cos 0) = 1 - (-1) = 2
have h := integral_eq_sub_of_hasDerivAt
  (f := fun x => -Real.cos x) (f' := Real.sin) ...
simp [Real.cos_zero, Real.cos_pi] at h  -- -(-1) - (-1) = 2
```