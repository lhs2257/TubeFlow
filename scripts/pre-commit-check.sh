#!/bin/bash
# PreToolUse hook (Bash): git commit 감지 시 문서 동기화 검증
# PROGRESS.md가 최신이 아니면 커밋을 물리적으로 차단합니다.

# stdin에서 hook input 읽기
INPUT=$(cat)

# 실행할 명령 추출
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# git commit 명령이 아니면 통과
if ! echo "$COMMAND" | grep -q "git commit"; then
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# PROJECT.md가 없으면 (초기화 전) 통과
if [ ! -f "$PROJECT_ROOT/PROJECT.md" ]; then
  exit 0
fi

# PROGRESS.md가 없으면 통과
if [ ! -f "$PROJECT_ROOT/PROGRESS.md" ]; then
  exit 0
fi

# PROGRESS.md보다 최근에 수정된 소스 파일 확인
RECENT_CHANGES=$(find "$PROJECT_ROOT" \
  -not -path "*/.claude/*" \
  -not -path "*/node_modules/*" \
  -not -path "*/research/*" \
  -not -path "*/templates/*" \
  -not -path "*/references/*" \
  -not -path "*/.git/*" \
  -not -name "PROGRESS.md" \
  -not -name "PROJECT.md" \
  -not -name "README.md" \
  -not -name "CLAUDE.md" \
  -not -name "*.template.md" \
  -newer "$PROJECT_ROOT/PROGRESS.md" \
  -type f 2>/dev/null | head -5)

if [ -n "$RECENT_CHANGES" ]; then
  # 커밋 차단: PROGRESS.md가 최신이 아님
  jq -n '{
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "deny",
      "permissionDecisionReason": "[커밋 차단] PROGRESS.md가 소스 파일보다 오래되었습니다. PROGRESS.md를 먼저 업데이트한 후 커밋하세요."
    }
  }'
  exit 0
fi

# 커밋 메시지 형식 검증: <타입>(<범위>): <요약> 또는 <타입>: <요약>
# sed 사용 (grep -oP는 macOS 기본 grep에서 미지원)
COMMIT_MSG=$(echo "$COMMAND" | sed -n 's/.*-m "\([^"]*\)".*/\1/p' 2>/dev/null)
if [ -z "$COMMIT_MSG" ]; then
  COMMIT_MSG=$(echo "$COMMAND" | sed -n "s/.*-m '\([^']*\)'.*/\1/p" 2>/dev/null)
fi

if [ -n "$COMMIT_MSG" ]; then
  # grep -E (Extended regex)로 이식성 확보 (macOS/Linux 모두 지원)
  if ! echo "$COMMIT_MSG" | grep -qE "^(기능|수정|문서|구조|설정|초기화)(\(.+\))?: .+" 2>/dev/null; then
    jq -n --arg msg "[커밋 차단] 커밋 메시지 형식이 올바르지 않습니다. 형식: <타입>(<범위>): <요약>  허용 타입: 기능, 수정, 문서, 구조, 설정, 초기화  예시: 기능(인증): 로그인 API 구현" '{
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": $msg
      }
    }'
    exit 0
  fi
fi

exit 0
