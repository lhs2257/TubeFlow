#!/bin/bash
# PreToolUse hook (Write|Edit): 이모지 사용 물리적 차단
# 파일 내용에 이모지가 포함되면 Write/Edit를 차단합니다.

# stdin에서 hook input 읽기
INPUT=$(cat)

# 내용 추출 (Write: content, Edit: new_string)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

CONTENT=""
if [ "$TOOL_NAME" = "Write" ]; then
  CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // empty' 2>/dev/null)
elif [ "$TOOL_NAME" = "Edit" ]; then
  CONTENT=$(echo "$INPUT" | jq -r '.tool_input.new_string // empty' 2>/dev/null)
fi

if [ -z "$CONTENT" ]; then
  exit 0
fi

# 이모지 감지 (python3 사용, 없으면 grep -P 시도)
HAS_EMOJI="no"

if command -v python3 &>/dev/null; then
  HAS_EMOJI=$(printf '%s' "$CONTENT" | python3 -c "
import sys, re
text = sys.stdin.buffer.read().decode('utf-8', errors='ignore')
emoji_re = re.compile('[\\U0001F600-\\U0001F64F\\U0001F300-\\U0001F5FF\\U0001F680-\\U0001F6FF\\U0001F1E0-\\U0001F1FF\\U00002702-\\U000027B0\\U0001F900-\\U0001F9FF\\U00002600-\\U000026FF\\U0001FA00-\\U0001FAFF]')
print('yes' if emoji_re.search(text) else 'no')
" 2>/dev/null || echo "no")
elif printf '%s' "$CONTENT" | grep -P '[\x{1F600}-\x{1F64F}\x{1F300}-\x{1F5FF}\x{1F680}-\x{1F6FF}]' > /dev/null 2>&1; then
  HAS_EMOJI="yes"
fi

if [ "$HAS_EMOJI" = "yes" ]; then
  jq -n '{
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "deny",
      "permissionDecisionReason": "[이모지 차단] 이모지 사용이 금지되어 있습니다. 텍스트 마커를 사용하세요: [완료], [진행중], [대기], [주의], [중요]"
    }
  }'
  exit 0
fi

exit 0
