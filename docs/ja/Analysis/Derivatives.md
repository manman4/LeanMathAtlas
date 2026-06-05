# 微分（導関数）

対応する Lean ファイル: `StudyLean4/Analysis/Derivatives.lean`

## `HasDerivAt` の読み方

```lean
HasDerivAt f f' a
```

「関数 f は点 a で微分可能で、f'(a) = f'」を意味する。

## 内容

### 基本的な導関数
| 定理名 | 内容 |
|--------|------|
| `deriv_const` | 定数関数の導関数は 0 |
| `deriv_id'` | 恒等関数の導関数は 1 |
| `deriv_pow'` | $\dfrac{d}{dx}[x^n] = n x^{n-1}$ |
| `deriv_sq` | $\dfrac{d}{dx}[x^2] = 2x$ |
| `deriv_cube` | $\dfrac{d}{dx}[x^3] = 3x^2$ |

### 微分の法則
| 定理名 | 内容 |
|--------|------|
| `deriv_add'` | 和の微分: $(f+g)' = f' + g'$ |
| `deriv_const_mul'` | 定数倍: $(cf)' = cf'$ |
| `deriv_mul'` | 積の微分: $(fg)' = f'g + fg'$ |
| `deriv_comp'` | 連鎖律: $(g \circ f)' = g'(f(a)) \cdot f'(a)$ |

### 具体的な応用
| 定理名 | 内容 |
|--------|------|
| `deriv_quadratic` | $\dfrac{d}{dx}[x^2+3x+1] = 2x+3$ |
| `deriv_product_example` | $\dfrac{d}{dx}[x(x+1)] = 2x+1$ |

### 三角関数の導関数
| 定理名 | 内容 |
|--------|------|
| `deriv_sin'` | $\dfrac{d}{dx}[\sin x] = \cos x$ |
| `deriv_cos'` | $\dfrac{d}{dx}[\cos x] = -\sin x$ |
| `deriv_sin_double` | $\dfrac{d}{dx}[\sin 2x] = 2\cos 2x$（連鎖律の応用） |
| `deriv_sin_cos` | $\dfrac{d}{dx}[\sin x \cos x] = \cos^2 x - \sin^2 x$（積の微分 → 2倍角公式） |

## 学習ポイント

- Lean の微分は「点 a での微分可能性と導関数値の同時表明」として `HasDerivAt` で表す。
- 連鎖律 `hg.comp a hf` は外側の微分情報 `hg` に対して `.comp` を呼ぶ。
- `simpa using hasDerivAt_pow n a` で $x^n$ の具体的な導関数を得られる。
