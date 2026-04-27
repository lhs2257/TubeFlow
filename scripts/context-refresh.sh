#!/bin/bash
# UserPromptSubmit hook: 매 5번째 프롬프트마다 핵심 규칙 재주입
# 대화가 길어질수록 CLAUDE.md 지침의 영향력이 줄어드는 문제를 보완합니다.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# PROJECT.md가 없으면 (초기화 전) 통과
if [ ! -f "$PROJECT_ROOT/PROJECT.md" ]; then
  exit 0
fi

# 프로젝트별 카운터 파일 경로
HASH=$(echo "$PROJECT_ROOT" | cksum | cut -d' ' -f1)
COUNTER_FILE="/tmp/claude-prompt-counter-$HASH"

# 카운터 읽기/증가
COUNT=0
if [ -f "$COUNTER_FILE" ]; then
  COUNT=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
fi
COUNT=$((COUNT + 1))
echo "$COUNT" > "$COUNTER_FILE"

# 5번째 프롬프트마다 핵심 규칙 재주입
if [ $((COUNT % 5)) -eq 0 ]; then
  RULES_FILE="$SCRIPT_DIR/core-rules.txt"
  if [ -f "$RULES_FILE" ]; then
    RULES=$(cat "$RULES_FILE")
    jq -n --arg rules "$RULES" '{
      "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": $rules
      }
    }'
  fi
fi

exit 0
