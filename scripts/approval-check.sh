#!/bin/bash
# Stop hook: 작업 완료 후 사용자 승인 요청 여부 확인
# 파일을 수정한 턴에서 사용자에게 다음 단계 확인을 구하지 않으면 차단합니다.

# stdin에서 hook input 읽기
INPUT=$(cat)

# stop_hook_active 확인 (무한루프 방지)
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null)
if [ "$STOP_HOOK_ACTIVE" = "true" ]; then
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

# 마지막 어시스턴트 메시지 추출
LAST_MSG=$(echo "$INPUT" | jq -r '.last_assistant_message // empty' 2>/dev/null)

if [ -z "$LAST_MSG" ]; then
  exit 0
fi

# 최근 2분 내 수정된 소스 파일이 있는지 확인 (작업이 수행된 턴인지 판별)
RECENT_WORK=$(find "$PROJECT_ROOT" \
  -not -path "*/.claude/*" \
  -not -path "*/node_modules/*" \
  -not -path "*/research/*" \
  -not -path "*/references/*" \
  -not -path "*/.git/*" \
  -not -name "*.template.md" \
  -newer "$PROJECT_ROOT/PROGRESS.md" \
  -type f -mmin -2 2>/dev/null | head -1)

# 최근 파일 수정이 없으면 (정보 응답 등) 통과
if [ -z "$RECENT_WORK" ]; then
  exit 0
fi

# 승인 요청 키워드 확인
if echo "$LAST_MSG" | grep -qE "(진행할까요|승인|확인해|어떻게 할까요|괜찮으시|시작할까요|다음 단계|알려주세요|말씀해|의견|어떻게 하시겠|원하시|검토|피드백)"; then
  exit 0  # 승인 요청이 포함됨 - 통과
fi

# 승인 요청이 없으면 차단
echo "[승인 누락] 작업 완료 후 사용자에게 다음 단계 진행 여부를 반드시 확인하세요. 예: '다음 작업을 진행할까요?'" >&2
exit 2
