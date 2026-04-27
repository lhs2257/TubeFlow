# script_writer/ - 대본 작성 모듈

## 개요

수집된 소재를 입력받아 Claude API를 통해 유튜브 대본을 자동 생성합니다.

## 주요 기능

- 소재 기반 대본 자동 생성 (Claude API)
- 대본 템플릿 관리 (인트로/아웃트로/본문)
- 생성된 대본 저장 및 편집

## 인터페이스

```python
generate_script(post: Post, template: str) -> Script
save_script(script: Script, path: str) -> str
```

## 필요 환경변수

```
ANTHROPIC_API_KEY=
```

## 상태

- [ ] 개발 예정 (M3 단계)
