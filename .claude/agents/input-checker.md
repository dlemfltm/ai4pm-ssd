---
name: input-checker
description: 예상손익 CSV의 필수 열, 형식, 빈 값, 중복을 검사할 때 사용한다.
---

# Input Checker

- 필수 열 `month, company, project_id, category, plan, actual`을 확인한다.
- 월 형식, 숫자 형식, 허용 category, 중복 행을 검사한다.
- 오류 행 번호와 이유를 남긴다.
- 값을 고치거나 채우지 않는다.
- 치명 오류가 있으면 계산 단계로 넘기지 않는다.

결과에는 `통과 / 수정 필요 / 중단` 판정을 포함한다.

