---
title: "plan=0 예외 처리"
type: concept
status: reviewed
evidence_tier: 2
confirmed_by: 이혜림
source_ids:
  - SRC-20260813-002
updated: 2026-08-14
---

# plan=0 예외 처리

## 한 줄 정의

계획이 0인 행은 차이율을 계산하지 않고 "확인 필요"로 남긴다.

## 확인된 내용

- 차이율 = 차이 ÷ 계획 × 100 인데, 계획이 0이면 0으로 나눌 수 없다. (근거: [[wiki/sources/SRC-20260813-002-variance-rule]])
- 임의로 0이나 무한대로 채우지 않고 "확인 필요"로 표시한다. (근거: [[wiki/sources/SRC-20260813-002-variance-rule]])

## 사용처

- `pnl-analyst` 계산 단계에서 `plan=0` 행을 만나면 차이율 칸에 "확인 필요"를 출력하도록 하는 규칙.

## 예외와 주의점

- 차이(실적−계획) 자체는 계산 가능하므로 표시하되, 차이'율'만 보류한다.
