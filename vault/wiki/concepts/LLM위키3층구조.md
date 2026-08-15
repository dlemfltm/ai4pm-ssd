---
title: "LLM Wiki 3층 구조"
type: concept
status: reviewed
evidence_tier: 1
confirmed_by: 이현옥
source_ids:
  - SRC-20260814-104
  - SRC-20260814-101
updated: 2026-08-14
---

# LLM Wiki 3층 구조

## 한 줄 정의

지식을 규칙 / 지식 / 원문 3층으로 나눠 AI와 사람이 함께 쓴다.

## 확인된 내용

- 원문/위키/스키마 3층 = `raw/`(원문) · `wiki/`(지식) · `CLAUDE.md`(규칙). (근거: [[wiki/sources/SRC-20260814-104-karpathy-llm-wiki]])
- `CLAUDE.md`는 세션마다 자동 로딩되는 규칙 층이다. (근거: [[wiki/sources/SRC-20260814-101-claude-code-docs]])

## 사용처

- 우리 vault 폴더 설계의 근거: `vault/raw` · `vault/wiki` · 루트 `CLAUDE.md`.

## 예외와 주의점

- 원문 층(raw)은 수정하지 않는다. → [[wiki/concepts/데이터무결성]]
