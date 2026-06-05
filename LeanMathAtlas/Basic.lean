/-
  # Lean 4 基本構文
  Lean 4 の基本的な構文と型システムを学ぶ
-/
import Mathlib.Tactic

-- ============================================================
-- 1. #check と #eval — 型と値の確認
-- ============================================================

-- #check は式の型を表示する（コンパイルはされない）
#check 42          -- 42 : Nat
#check "hello"     -- "hello" : String
#check true        -- true : Bool
#check (1 : Int)   -- 1 : Int

-- #eval は式を評価して結果を表示する
#eval 2 + 3        -- 5
#eval "Hello" ++ " " ++ "Lean 4!"  -- "Hello Lean 4!"
#eval (10 : Nat) / 3   -- 3（自然数の除算は切り捨て）

-- ============================================================
-- 2. 基本型
-- ============================================================

-- Nat : 自然数（0, 1, 2, ...）
#check (0 : Nat)
#eval (7 : Nat)

-- Int : 整数（..., -2, -1, 0, 1, 2, ...）
#check (-3 : Int)
#eval (-3 : Int) + 5  -- 2

-- Bool : 真偽値
#check true
#check false
#eval true && false   -- false
#eval true || false   -- true
#eval !true           -- false

-- String : 文字列
#check "Lean 4"
#eval "abc".length    -- 3

-- Prop : 命題の型（True/False ではなく、証明可能性を表す）
#check (1 = 1)        -- 1 = 1 : Prop
#check (2 < 5)        -- 2 < 5 : Prop

-- ============================================================
-- 3. 定義 (def)
-- ============================================================

-- 値の定義
def myNumber : Nat := 42
#eval myNumber  -- 42

-- 関数の定義
def double (n : Nat) : Nat := 2 * n
#eval double 5  -- 10

-- 複数引数の関数
def add (a b : Nat) : Nat := a + b
#eval add 3 7   -- 10

-- 型推論：型注釈を省略できる場合がある
def triple (n : Nat) := 3 * n
#eval triple 4  -- 12

-- ============================================================
-- 4. if 式と match 式
-- ============================================================

-- if 式（Lean では式なので値を返す）
def isPositive (n : Int) : Bool :=
  if n > 0 then true else false

#eval isPositive 5    -- true
#eval isPositive (-3) -- false

-- match 式（パターンマッチ）
def describe (n : Nat) : String :=
  match n with
  | 0 => "zero"
  | 1 => "one"
  | _ => "many"

#eval describe 0  -- "zero"
#eval describe 1  -- "one"
#eval describe 5  -- "many"

-- ============================================================
-- 5. 構造体 (structure)
-- ============================================================

-- 構造体の定義
structure Point where
  x : Float
  y : Float

-- 構造体のインスタンス作成
def origin : Point := { x := 0.0, y := 0.0 }
def p1 : Point := { x := 1.0, y := 2.0 }

-- フィールドへのアクセス
#eval p1.x  -- 1.0
#eval p1.y  -- 2.0

-- ============================================================
-- 6. リスト
-- ============================================================

-- リストの作成
def myList : List Nat := [1, 2, 3, 4, 5]

#eval myList          -- [1, 2, 3, 4, 5]
#eval myList.length   -- 5
#eval myList.head?    -- some 1
#eval myList.tail     -- [2, 3, 4, 5]
#eval myList.reverse  -- [5, 4, 3, 2, 1]

-- リストの連結
#eval [1, 2] ++ [3, 4]  -- [1, 2, 3, 4]

-- cons 演算子（先頭に要素を追加）
#eval 0 :: [1, 2, 3]    -- [0, 1, 2, 3]

-- ============================================================
-- 7. let 式（ローカル束縛）
-- ============================================================

def computeArea (width height : Nat) : Nat :=
  let area := width * height
  let doubled := area * 2
  doubled

#eval computeArea 3 4  -- 24

-- ============================================================
-- 8. 再帰関数
-- ============================================================

-- 階乗（再帰で定義）
def factorial : Nat → Nat
  | 0 => 1
  | n + 1 => (n + 1) * factorial n

#eval factorial 5   -- 120
#eval factorial 10  -- 3628800

-- フィボナッチ数
def fibonacci : Nat → Nat
  | 0 => 0
  | 1 => 1
  | n + 2 => fibonacci (n + 1) + fibonacci n

#eval fibonacci 10  -- 55
