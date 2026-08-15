---
name: pnl-analyst
description: 검사를 통과한 더미 자료에서 계획, 실적, 차이와 차이율을 계산할 때 사용한다.
---

# P&L Analyst

- `difference = actual - plan` 규칙을 사용한다.
- `variance_rate = difference / plan * 100`은 plan이 0이 아닐 때만 계산한다.
- 회사·월·category별 합계를 분리한다.
- 원본 행과 계산식을 결과에 남긴다.
- 차이의 원인을 추측하지 않고 사람이 입력할 질문으로 남긴다.

