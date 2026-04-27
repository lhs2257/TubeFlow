#!/bin/bash
# PostToolUse hook: Write|Edit 후 문서 업데이트 리마인더
# JSON additionalContext로 Claude에게 직접 전달합니다.

# stdin에서 hook input 읽기
INPUT=$(cat)

# 수정된 파일 경로 추출
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# templates/, research/, .claude/, references/ 폴더 내 파일은 무시
case "$FILE_PATH" in
  */templates/*|*/research/*|*/.claude/*|*/node_modules/*|*/references/*)
    exit 0
    ;;
esac

# PROGRESS.md, PROJECT.md, CLAUDE.md 자체 수정은 무시
BASENAME=$(basename "$FILE_PATH")
case "$BASENAME" in
  PROGRESS.md|PROJECT.md|CLAUDE.md)
    exit 0
    ;;
esac

# 해당 파일이 속한 모듈의 README.md 경로 찾기
DIR=$(dirname "$FILE_PATH")
MODULE_README=""
while [ "$DIR" != "/" ] && [ "$DIR" != "." ]; do
  if [ -f "$DIR/README.md" ]; then
    MODULE_README="$DIR/README.md"
    break
  fi
  DIR=$(dirname "$DIR")
done

# additionalContext를 JSON으로 반환
MSG="[문서 업데이트 리마인더] $FILE_PATH 가 수정되었습니다."
if [ -n "$MODULE_README" ]; then
  MSG="$MSG 관련 문서도 업데이트하세요: $MODULE_README, PROGRESS.md"
else
  MSG="$MSG PROGRESS.md를 업데이트하세요."
fi

jq -n --arg msg "$MSG" '{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": $msg
  }
}'

exit 0
