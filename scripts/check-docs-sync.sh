#!/bin/bash
# Stop hook: 매 턴 종료 시 문서 동기화 상태 확인
# exit 2 + stderr로 Claude의 종료를 차단하고 문서 업데이트를 강제합니다.

# stdin에서 hook input 읽기
INPUT=$(cat)

# stop_hook_active 확인 (무한루프 방지)
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null)
if [ "$STOP_HOOK_ACTIVE" = "true" ]; then
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# PROJECT.md가 없으면 (초기화 전) 체크 불필요
if [ ! -f "$PROJECT_ROOT/PROJECT.md" ]; then
  exit 0
fi

# PROGRESS.md가 없으면 체크 불필요
if [ ! -f "$PROJECT_ROOT/PROGRESS.md" ]; then
  exit 0
fi

ISSUES=""

# 최근 수정된 소스 파일 확인 (PROGRESS.md보다 새로운 파일)
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
  ISSUES="[문서 동기화 필요] 다음 파일들이 PROGRESS.md보다 최근에 수정되었습니다:"
  while IFS= read -r file; do
    ISSUES="$ISSUES | - $file"
  done <<< "$RECENT_CHANGES"
  ISSUES="$ISSUES | PROGRESS.md를 최신 상태로 업데이트한 후 종료하세요."
fi

# git 저장소인 경우 uncommitted changes 확인
if git -C "$PROJECT_ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  UNCOMMITTED=$(git -C "$PROJECT_ROOT" status --porcelain 2>/dev/null | head -1)
  if [ -n "$UNCOMMITTED" ]; then
    ISSUES="$ISSUES${ISSUES:+ | }[커밋 필요] 커밋되지 않은 변경사항이 있습니다. 변경사항을 커밋한 후 종료하세요."
  fi
fi

# 이슈가 있으면 stderr로 출력하고 exit 2로 차단
if [ -n "$ISSUES" ]; then
  echo "$ISSUES" >&2
  exit 2
fi

exit 0
