# 三角関数の公式

対応する Lean ファイル: `StudyLean4/Analysis/Trigonometry.lean`

## 内容

### 数学 I — 基本公式
| 定理名 | 内容 |
|--------|------|
| `pythagorean` | $\sin^2 x + \cos^2 x = 1$ |
| `cos_sq_eq` | $\cos^2 x = 1 - \sin^2 x$ |
| `sin_sq_eq` | $\sin^2 x = 1 - \cos^2 x$ |
| `tan_def` | $\tan x = \sin x / \cos x$ |
| `one_add_tan_sq` | $1 + \tan^2 x = 1/\cos^2 x$ |

### 数学 II — 加法定理
| 定理名 | 内容 |
|--------|------|
| `sin_add_formula` | $\sin(x+y) = \sin x\cos y + \cos x\sin y$ |
| `cos_add_formula` | $\cos(x+y) = \cos x\cos y - \sin x\sin y$ |
| `sin_sub_formula` | $\sin(x-y) = \sin x\cos y - \cos x\sin y$ |
| `cos_sub_formula` | $\cos(x-y) = \cos x\cos y + \sin x\sin y$ |

### 数学 II — 2倍角公式
| 定理名 | 内容 |
|--------|------|
| `sin_double` | $\sin 2x = 2\sin x\cos x$ |
| `cos_double` | $\cos 2x = \cos^2 x - \sin^2 x$ |
| `cos_double_sin` | $\cos 2x = 1 - 2\sin^2 x$ |
| `cos_double_cos` | $\cos 2x = 2\cos^2 x - 1$ |

### 数学 I — 特殊値
| 定理名 | 内容 |
|--------|------|
| `sin_zero`, `cos_zero` | $\sin 0=0,\ \cos 0=1$ |
| `sin_pi_div_two`, `cos_pi_div_two` | $\sin(\pi/2)=1,\ \cos(\pi/2)=0$ |
| `sin_pi`, `cos_pi` | $\sin\pi=0,\ \cos\pi=-1$ |
