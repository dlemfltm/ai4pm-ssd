---
title: "Claude Code 공식 문서"
type: source
status: reviewed
evidence_tier: 1
confirmed_by: 이현옥
source_ids:
  - SRC-20260814-101
updated: 2026-08-14
---

# Claude Code 공식 문서

## 원문

- 원문 파일: [[raw/SRC-20260814-101-claude-code-docs]]
- 링크: https://code.claude.com/docs/en/memory
- 확인일: 2026-08-14 · 확인자: 이현옥 · 성격: 공식 문서

## 이 자료로 답할 질문

- LLM Wiki의 규칙(CLAUDE.md)·역할 분리(subagent)·워크플로우(skill)를 어떤 형식으로 만드는가?

## 확인된 내용

- CLAUDE.md는 세션마다 자동 로딩되는 프로젝트 규칙이다. (Memory)
- Subagent는 `.claude/agents/*.md`에 YAML로 정의하고 별도 컨텍스트를 가진다. (Sub-agents)
- Skill은 `.claude/skills/*/SKILL.md`로 워크플로우를 패키지화한다. (Skills)

## 사용처

- `CLAUDE.md`에 예상손익 규칙을 담아 매 작업에 적용, 검사·계산·검토를 subagent로 분리하는 설계 근거.

## 관련 문서

- [[wiki/concepts/LLM위키3층구조]]
- [[wiki/concepts/근거추적검증]]
