#!/bin/sh
# PreToolUse hook: 危険なBashコマンドをブロック
# Claude Code から stdin に JSON { "tool_name": "Bash", "tool_input": { "command": "..." } } が渡される

cmd=$(python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)

# Force push (フラグ位置・スペルに依存しない)
if echo "$cmd" | grep -qE 'git\s+push' && \
   echo "$cmd" | grep -qE '(--force|--force-with-lease|-[a-zA-Z]*f|\+[^[:space:]]+:)'; then
  echo "BLOCKED: force push (--force / -f / +refspec) は禁止です" >&2
  exit 1
fi

# rm with recursive + force (順不同・結合フラグ対応)
if echo "$cmd" | grep -qE '\brm\b'; then
  has_r=$(echo "$cmd" | grep -cE '\-[a-zA-Z]*[rR]|\-\-recursive')
  has_f=$(echo "$cmd" | grep -cE '\-[a-zA-Z]*f|\-\-force')
  if [ "$has_r" -gt 0 ] && [ "$has_f" -gt 0 ]; then
    echo "BLOCKED: rm -rf 系コマンドは禁止です" >&2
    exit 1
  fi
fi

# ダウンロード → 実行のパイプライン
if echo "$cmd" | grep -qE '\b(curl|wget|fetch|aria2c)\b' && \
   echo "$cmd" | grep -qE '\b(bash|sh|zsh|fish|python3?|node|perl|ruby|eval|source)\b'; then
  echo "BLOCKED: スクリプトのダウンロード実行は禁止です" >&2
  exit 1
fi

# シークレットファイルへのBashアクセス
if echo "$cmd" | grep -qE '\b(cat|less|head|tail|grep|more|xxd|base64|tar|cp|mv|scp|rsync)\b' && \
   echo "$cmd" | grep -qE '(\.env|secrets\.|/\.ssh/|/\.gnupg/)'; then
  echo "BLOCKED: シークレットファイルへのアクセスは禁止です" >&2
  exit 1
fi

exit 0
