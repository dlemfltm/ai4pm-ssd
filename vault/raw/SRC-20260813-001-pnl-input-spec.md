# 원문 · 예상손익 입력 CSV 명세 (더미)

- 성격: 내부 가이드 (더미 자료)
- 수집일: 2026-08-13
- 비고: 실제 기업 수치가 아닌 학습용 더미 자료다.

## 열 정의

| 열 | 의미 | 형식 |
|---|---|---|
| month | 기준월 | YYYY-MM |
| company | 법인명 | 문자열 |
| project_id | 프로젝트 번호 | 문자열 |
| category | 계정 구분 | revenue / cost / expense |
| plan | 계획 금액 | 정수 |
| actual | 실적 금액 | 정수 |

## 샘플 행

```
2026-08,Demo Alpha,P-101,revenue,120000,115000
2026-08,Demo Alpha,P-101,cost,72000,76000
2026-08,Demo Alpha,P-101,expense,18000,17500
2026-08,Demo Beta,P-202,revenue,90000,96000
2026-08,Demo Beta,P-202,cost,54000,56000
2026-08,Demo Beta,P-202,expense,12000,12000
```

## 규칙 (원문 명시)

- 빈 값을 0으로 추측하지 않는다.
- 입력 원본을 수정하지 않는다.
- 허용 category 외 값은 오류로 표시한다.
