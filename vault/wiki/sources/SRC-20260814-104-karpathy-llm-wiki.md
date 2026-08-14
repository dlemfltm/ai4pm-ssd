---
title: "Karpathy LLM Wiki (Gist)"
type: source
status: reviewed
evidence_tier: 1
confirmed_by: 조장
source_ids:
  - SRC-20260814-104
updated: 2026-08-14
---

# Karpathy LLM Wiki (Gist)

## 원문

- 원문 파일: [[raw/SRC-20260814-104-karpathy-llm-wiki]]
- 링크: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- 확인일: 2026-08-14 · 확인자: 조장 · 성격: 방법론 원저(1차 자료)

## 이 자료로 답할 질문

- AI가 다시 쓸 수 있는 지식베이스는 어떤 구조와 운영 흐름으로 만드는가?

## 확인된 내용

- 원문/위키/스키마 **3층**(raw · wiki · CLAUDE.md)으로 나눈다.
- 운영은 **Ingest → Query → Lint** 사이클로 돈다.
- 사람은 원문 선별·분석 지시·질문을, LLM은 요약·연결·정리를 맡는다.

## 사용처

- 우리 vault의 3층 구조와 Ingest/Query/Lint(+사람 Review) 운영 방식의 직접 근거.

## 관련 문서

- [[wiki/concepts/LLM위키3층구조]]
- [[wiki/concepts/근거추적검증]]
