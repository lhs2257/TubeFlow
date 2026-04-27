# 범용 클로드코드 프로젝트 템플릿

## 개요

이 템플릿은 Claude Code로 어떤 프로젝트든 최적으로 시작할 수 있도록 설계된 **meta-template**입니다.

복제 후 Claude Code를 실행하면, 자동으로 온보딩 프로세스가 시작되어:
1. 프로젝트 목적과 업무 유형을 파악하고
2. 해당 분야에 맞는 방법론과 구조를 리서치하고
3. 최적의 폴더 구조와 규칙을 제안/승인 후 세팅합니다

## 사용법

### 1. 템플릿 복제
```bash
cp -r "범용 클로드코드 템플릿" "새-프로젝트명"
cd "새-프로젝트명"
```

### 2. Claude Code 실행
```bash
claude
```
또는 VS Code에서 Claude Code 확장으로 실행

### 3. 자동 온보딩
Claude Code가 CLAUDE.md를 읽고 자동으로 5단계 온보딩을 시작합니다:
- 1단계: 프로젝트 파악 (목적, 유형, 기술 스택 질문)
- 2단계: 맞춤 리서치 (방법론, 구조, 베스트 프랙티스)
- 3단계: 구조/방법론 제안 (사용자 승인)
- 4단계: 프로젝트 세팅 (폴더, 문서, 설정)
- 5단계: 업무 시작 준비 완료

### 4. 커스텀 커맨드 활용
- `/project:init` - 초기화 재실행
- `/project:status` - 현황 확인
- `/project:next` - 다음 작업 진행
- `/project:review` - 전체 검토
- `/project:resume` - 이전 세션 복원 (git log + PROGRESS.md 기반)

## 템플릿 구조

```
범용 클로드코드 템플릿/
  CLAUDE.md                    # 온보딩 프로세스 및 핵심 원칙 정의
  README.md                    # 현재 파일 (템플릿 사용 안내)
  .gitignore                   # Git 제외 파일 목록
  .claude/
    settings.json              # Claude Code 설정 (hooks, 권한, 보안)
    commands/
      init.md                  # /project:init 커맨드
      status.md                # /project:status 커맨드
      next.md                  # /project:next 커맨드
      review.md                # /project:review 커맨드
      resume.md                # /project:resume 커맨드 (세션 복원)
  scripts/
    pre-commit-check.sh        # PreToolUse hook: 커밋 전 문서 동기화 + 메시지 형식 검증
    emoji-check.sh             # PreToolUse hook: 이모지 사용 차단
    doc-update-reminder.sh     # PostToolUse hook: 문서 업데이트 리마인더
    check-docs-sync.sh         # Stop hook: 문서 동기화 + uncommitted changes 검증
    approval-check.sh          # Stop hook: 사용자 승인 요청 여부 확인
    context-refresh.sh         # UserPromptSubmit hook: 핵심 규칙 주기적 재주입
    core-rules.txt             # 핵심 규칙 압축본 (context-refresh.sh용)
  templates/
    PROJECT.template.md        # 프로젝트 개요 문서 템플릿
    PROGRESS.template.md       # 작업 현황 추적 문서 템플릿
    MODULE-README.template.md  # 모듈별 README 템플릿
    SPEC.template.md           # 기능 명세 템플릿
  research/                    # 리서치 결과 저장 (기능별 모듈화)
    01-claude-code-config/     # Claude Code 설정 관련 리서치
    02-methodology/            # 방법론 관련 리서치
    03-ai-tool-analysis/       # AI 도구 비교 분석
```

## 핵심 철학

1. **일 쪼개기**: 모든 업무를 단계별 분해, 순차 진행, 단계별 승인
2. **문서화 필수**: 코드 변경 시 문서 동시 업데이트 (hooks로 강제)
3. **모듈화**: 기능 단위 독립 모듈, 교차 의존 최소화
4. **투명한 현황**: PROGRESS.md에 항상 현재 상태 반영
5. **엄격한 네이밍**: 일관된 명명 규칙으로 누구나 구조 파악 가능

## 주의사항

- `system-prompts-and-models-of-ai-tools-main/` 폴더는 레퍼런스 자료입니다. 새 프로젝트에는 복제하지 않아도 됩니다.
- `research/` 폴더의 기존 리서치는 템플릿 설계를 위한 것입니다. 새 프로젝트의 리서치는 초기화 시 새로 수행됩니다.
- hooks 스크립트(`scripts/`)는 bash 환경과 `jq`가 필요합니다. Windows에서는 Git Bash가 설치되어 있어야 합니다.
- macOS에서는 `brew install jq`로 설치할 수 있습니다. Linux에서는 `apt install jq` 또는 `yum install jq`를 사용합니다.
