---
title: "예상손익 입력 CSV 명세"
type: source
status: reviewed
source_ids:
  - SRC-20260813-001
updated: 2026-08-13
---

# 예상손익 입력 CSV 명세

## 원문

- 원문 파일: [[raw/SRC-20260813-001-pnl-input-spec]]
- 확인일: 2026-08-13
- 확인자: 조원A
- 자료 성격: 가이드 (더미)

## 이 자료로 답할 질문

- 예상손익 보고서를 만들려면 입력 파일에 어떤 열이 어떤 형식으로 있어야 하는가?

## 확인된 내용

- 필수 열은 `month, company, project_id, category, plan, actual` 이다. (원문 "열 정의" 표)
- category 허용값은 revenue / cost / expense 세 가지다. (원문 "열 정의" 표)
- 빈 값을 0으로 추측하지 않는다. (원문 "규칙" 1항)
- 입력 원본을 수정하지 않는다. (원문 "규칙" 2항)

## 프로젝트 적용 후보

- input-checker가 필수 열·형식·허용 category를 우선 검사하도록 한다.

## 충돌 또는 확인 필요

- actual 빈 값 처리 방식은 이 원문에 없음 → 담당자 확인 필요.

## 관련 문서

- [[wiki/concepts/차이율]]
- [[wiki/projects/예상손익-보고서]]
