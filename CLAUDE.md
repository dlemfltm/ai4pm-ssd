# Forecast P&L Project Rules

## Goal

더미 CSV 1개를 읽어 계획·실적·차이·오류·사람 확인이 있는 Markdown 보고서 1개를 만든다.

## Read first

1. `README.md`
2. `samples/input/project_pnl_sample.csv`
3. `samples/expected/forecast-pnl-report.md`
4. `tests/eval-cases.md`

## Rules

- 입력 원본을 수정하지 않는다.
- 빈 값을 0으로 추측하지 않는다.
- 모든 계산은 입력 행으로 추적할 수 있어야 한다.
- 계획이 0이면 차이율을 임의 계산하지 않고 확인 필요로 표시한다.
- 실제 기업 수치와 식별정보를 요청하거나 저장하지 않는다.
- SAP·외부 시스템에 연결하거나 자동 승인하지 않는다.
- 결과는 `outputs/`에만 저장한다.

## Done

실제 실행 결과, Reviewer 의견, 사람 확인 목록, Test Log가 있어야 완료다.

