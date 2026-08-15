---
name: forecast-pnl
description: 더미 프로젝트 예상손익 자료의 입력 검사, 차이 계산, Reviewer 검토, 사람 승인 목록을 생성한다.
---

# Forecast P&L Workflow

1. `CLAUDE.md`와 Sample, Expected Output, Test를 읽는다.
2. input-checker가 입력을 검사한다. 치명 오류면 중단 보고서를 만든다.
3. pnl-analyst가 계획·실적·차이·차이율을 계산한다.
4. 회사·월별 요약과 확인 필요를 `outputs/forecast-pnl-report.md`에 쓴다.
5. finance-reviewer가 계산과 근거를 다시 확인한다.
6. 필수 수정은 최대 2회 반영하고, 남은 차이는 알려진 한계로 남긴다.
7. 실행한 Test와 사람 승인 항목을 결과에 포함한다.

## Fallback

- Excel 처리 실패 → 제공 CSV 사용
- 여러 회사 처리 실패 → 회사 1개로 축소
- 차이 기준 미확정 → 수치만 표시하고 담당자 확인

