# 원문 요지 · Claude Code 공식 문서

- 출처: https://code.claude.com/docs/en/memory (Memory) · /sub-agents · /skills
- 확인일: 2026-08-14 · 확인자: 이현옥 · 성격: 공식 문서
- ※ 아래는 원문을 읽고 요약한 사실 메모(발췌 아님).

## 확인된 사실

- **CLAUDE.md**: 프로젝트별 지시를 담는 파일로, 세션마다 자동으로 읽힌다. 위치는 `./CLAUDE.md`, `.claude/`, 사용자 수준 `~/.claude/CLAUDE.md`.
- **Subagents**: 특정 작업을 처리하는 전문 보조자. `.claude/agents/*.md`에 YAML frontmatter(name·description·tools·시스템 프롬프트)로 정의하며, 별도 컨텍스트 창을 가진다.
- **Skills**: `.claude/skills/*/SKILL.md`로 반복 워크플로우를 패키지화해 Claude 기능을 확장한다.
