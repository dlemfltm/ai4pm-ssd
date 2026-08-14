# wiki_lint.py 실행 로그

- 명령: `python scripts/wiki_lint.py vault`
- Python: 3.13.15

## 2차 실행 · 2026-08-14 (팀원 승격 후 재검증)

차이율·예상손익-보고서 노트를 `reviewed`로 승격한 뒤 재실행.

```
LLM Wiki 점검 결과
- Wiki 문서: 6
- Raw 원문: 2
- Wikilink: 17
- 오류: 0
- 경고: 0

PASS: 기본 형식과 연결 상태가 정상입니다.
```

## 1차 실행 · 2026-08-13 (최초 검증)

```
LLM Wiki 점검 결과
- Wiki 문서: 6
- Raw 원문: 2
- Wikilink: 17
- 오류: 0
- 경고: 0

PASS: 기본 형식과 연결 상태가 정상입니다.
```

## 의미

- 모든 wiki 문서에 필수 속성(title·type·status·source_ids·updated)이 있음
- 끊어진 위키링크 없음, index.md에서 모든 문서로 링크됨(고립 문서 없음)
- source 문서가 raw 원문으로 연결되고, 참조된 출처번호(SRC-...)가 모두 존재함
