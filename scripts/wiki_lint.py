#!/usr/bin/env python3
"""Obsidian LLM Wiki의 기본 형식과 연결 상태를 점검한다.

외부 패키지 없이 실행할 수 있다.

사용법:
    python3 scripts/wiki_lint.py
    python3 scripts/wiki_lint.py /path/to/vault
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote


REQUIRED_KEYS = ("title", "type", "status", "updated")
SOURCE_REQUIRED_TYPES = {"source", "concept", "project", "decision", "comparison"}
ALLOWED_TYPES = SOURCE_REQUIRED_TYPES | {"index", "log"}
ALLOWED_STATUSES = {"needs-review", "reviewed", "active"}
SOURCE_ID_PATTERN = re.compile(r"^SRC-\d{8}-\d{3}$")
WIKILINK_PATTERN = re.compile(r"!?\[\[([^\]]+)\]\]")
LOG_ENTRY_PATTERN = re.compile(
    r"^## \[\d{4}-\d{2}-\d{2}\] (ingest|query|promote|lint) \| .+$"
)


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    path: str
    message: str


@dataclass(frozen=True)
class AuditResult:
    issues: tuple[Issue, ...]
    wiki_pages: int
    raw_sources: int
    wikilinks: int

    @property
    def errors(self) -> tuple[Issue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "ERROR")

    @property
    def warnings(self) -> tuple[Issue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "WARN")


def _display_path(path: Path, vault_root: Path) -> str:
    try:
        return path.relative_to(vault_root).as_posix()
    except ValueError:
        return path.as_posix()


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, object] | None, str]:
    """지원하는 단순 YAML frontmatter를 파싱한다.

    이 스타터의 속성은 scalar와 list만 사용하므로 PyYAML이 필요하지 않다.
    """

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, text

    data: dict[str, object] = {}
    current_list: str | None = None

    for raw_line in lines[1:end]:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        list_match = re.match(r"^\s+-\s+(.+)$", raw_line)
        if list_match and current_list:
            values = data.setdefault(current_list, [])
            if isinstance(values, list):
                values.append(_strip_quotes(list_match.group(1)))
            continue

        key_match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", raw_line)
        if not key_match:
            current_list = None
            continue

        key, raw_value = key_match.groups()
        raw_value = (raw_value or "").strip()
        if raw_value == "":
            data[key] = []
            current_list = key
        elif raw_value == "[]":
            data[key] = []
            current_list = None
        else:
            data[key] = _strip_quotes(raw_value)
            current_list = None

    body = "\n".join(lines[end + 1 :])
    return data, body


def extract_wikilinks(text: str) -> list[str]:
    return [match.group(1).strip() for match in WIKILINK_PATTERN.finditer(text)]


def _base_link_target(link: str) -> str:
    target = link.split("|", 1)[0].strip()
    target = target.split("#", 1)[0].strip()
    target = target.split("^", 1)[0].strip()
    return unquote(target).lstrip("/")


def _markdown_files(vault_root: Path) -> list[Path]:
    return sorted(
        path
        for path in vault_root.rglob("*.md")
        if not any(part.startswith(".") for part in path.relative_to(vault_root).parts)
    )


def _resolve_link(
    link: str,
    vault_root: Path,
    all_files: set[Path],
    by_stem: dict[str, list[Path]],
) -> tuple[Path | None, str | None]:
    target = _base_link_target(link)
    if not target:
        return None, None
    if "://" in target or target.startswith("mailto:"):
        return None, None

    suffix = Path(target).suffix.lower()
    if suffix and suffix != ".md":
        return None, None

    if "/" in target:
        candidate = vault_root / target
        if candidate.suffix.lower() != ".md":
            candidate = candidate.with_suffix(".md")
        candidate = candidate.resolve()
        return (candidate, None) if candidate in all_files else (None, "missing")

    stem = Path(target).stem
    candidates = by_stem.get(stem, [])
    if len(candidates) == 1:
        return candidates[0], None
    if len(candidates) > 1:
        return None, "ambiguous"
    return None, "missing"


def _as_source_ids(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str) and value:
        return [value]
    return []


def _valid_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))
    except ValueError:
        return False


def audit_vault(vault_root: Path) -> AuditResult:
    vault_root = vault_root.expanduser().resolve()
    issues: list[Issue] = []

    if not vault_root.is_dir():
        issues.append(Issue("ERROR", "VAULT_NOT_FOUND", str(vault_root), "Vault 폴더가 없습니다."))
        return AuditResult(tuple(issues), 0, 0, 0)

    wiki_root = vault_root / "wiki"
    raw_root = vault_root / "raw"
    wiki_files = sorted(wiki_root.rglob("*.md")) if wiki_root.is_dir() else []
    raw_files = sorted(raw_root.rglob("*.md")) if raw_root.is_dir() else []
    all_files_list = _markdown_files(vault_root)
    all_files = {path.resolve() for path in all_files_list}
    by_stem: dict[str, list[Path]] = defaultdict(list)
    for path in all_files:
        by_stem[path.stem].append(path)

    if not wiki_files:
        issues.append(Issue("ERROR", "WIKI_EMPTY", "wiki", "Wiki Markdown 문서가 없습니다."))

    page_meta: dict[Path, dict[str, object]] = {}
    page_links: dict[Path, list[str]] = {}
    resolved_links: dict[Path, set[Path]] = defaultdict(set)
    inbound: dict[Path, int] = defaultdict(int)
    known_source_ids: set[str] = set()
    total_links = 0

    for path in wiki_files:
        resolved_path = path.resolve()
        rel = _display_path(path, vault_root)
        text = path.read_text(encoding="utf-8")
        metadata, _ = parse_frontmatter(text)
        page_links[resolved_path] = extract_wikilinks(text)
        total_links += len(page_links[resolved_path])

        if metadata is None:
            issues.append(Issue("ERROR", "FRONTMATTER_MISSING", rel, "YAML 속성이 없거나 닫히지 않았습니다."))
            metadata = {}
        page_meta[resolved_path] = metadata

        for key in REQUIRED_KEYS:
            if key not in metadata or metadata[key] in ("", []):
                issues.append(Issue("ERROR", "PROPERTY_MISSING", rel, f"필수 속성 `{key}`가 없습니다."))

        page_type = str(metadata.get("type", ""))
        status = str(metadata.get("status", ""))
        if page_type and page_type not in ALLOWED_TYPES:
            issues.append(Issue("ERROR", "TYPE_INVALID", rel, f"지원하지 않는 type `{page_type}`입니다."))
        if status and status not in ALLOWED_STATUSES:
            issues.append(Issue("ERROR", "STATUS_INVALID", rel, f"지원하지 않는 status `{status}`입니다."))
        if metadata.get("updated") and not _valid_date(metadata.get("updated")):
            issues.append(Issue("ERROR", "DATE_INVALID", rel, "updated는 YYYY-MM-DD 형식이어야 합니다."))

        source_ids = _as_source_ids(metadata.get("source_ids"))
        if page_type in SOURCE_REQUIRED_TYPES and not source_ids:
            issues.append(Issue("ERROR", "SOURCE_IDS_MISSING", rel, "근거 문서에는 source_ids가 필요합니다."))
        for source_id in source_ids:
            if not SOURCE_ID_PATTERN.fullmatch(source_id):
                issues.append(Issue("ERROR", "SOURCE_ID_INVALID", rel, f"출처 번호 `{source_id}` 형식이 잘못되었습니다."))
        if page_type == "source":
            known_source_ids.update(source_ids)

    for path, links in page_links.items():
        rel = _display_path(path, vault_root)
        for link in links:
            resolved, problem = _resolve_link(link, vault_root, all_files, by_stem)
            if problem == "missing":
                issues.append(Issue("ERROR", "LINK_BROKEN", rel, f"대상 문서를 찾을 수 없습니다: [[{link}]]"))
            elif problem == "ambiguous":
                issues.append(Issue("WARN", "LINK_AMBIGUOUS", rel, f"같은 이름의 문서가 여러 개입니다: [[{link}]]"))
            elif resolved is not None:
                resolved_links[path].add(resolved)
                inbound[resolved] += 1

    for path, metadata in page_meta.items():
        rel = _display_path(path, vault_root)
        page_type = str(metadata.get("type", ""))
        source_ids = _as_source_ids(metadata.get("source_ids"))
        if page_type != "source":
            for source_id in source_ids:
                if SOURCE_ID_PATTERN.fullmatch(source_id) and source_id not in known_source_ids:
                    issues.append(Issue("ERROR", "SOURCE_UNKNOWN", rel, f"Source 문서가 없는 출처 번호입니다: {source_id}"))

        if page_type == "source":
            has_raw_link = any(
                target == raw_root.resolve() or raw_root.resolve() in target.parents
                for target in resolved_links.get(path, set())
            )
            if not has_raw_link:
                issues.append(Issue("ERROR", "SOURCE_NO_RAW", rel, "Source 문서에서 raw 원문으로 가는 링크가 없습니다."))

    index_path = (wiki_root / "index.md").resolve()
    if index_path not in page_meta:
        issues.append(Issue("ERROR", "INDEX_MISSING", "wiki/index.md", "index.md가 없습니다."))
        index_targets: set[Path] = set()
    else:
        index_targets = resolved_links.get(index_path, set())

    for path, metadata in page_meta.items():
        page_type = str(metadata.get("type", ""))
        rel = _display_path(path, vault_root)
        if page_type not in {"index", "log"} and path not in index_targets:
            issues.append(Issue("ERROR", "INDEX_GAP", rel, "index.md에 이 문서의 링크가 없습니다."))
        if page_type not in {"index", "log"} and inbound[path] == 0:
            issues.append(Issue("WARN", "ORPHAN", rel, "다른 Wiki 문서에서 들어오는 링크가 없습니다."))

    log_path = (wiki_root / "log.md").resolve()
    if log_path not in page_meta:
        issues.append(Issue("ERROR", "LOG_MISSING", "wiki/log.md", "log.md가 없습니다."))
    else:
        log_text = log_path.read_text(encoding="utf-8")
        for line_number, line in enumerate(log_text.splitlines(), start=1):
            if line.startswith("## ") and not LOG_ENTRY_PATTERN.fullmatch(line):
                issues.append(
                    Issue(
                        "WARN",
                        "LOG_FORMAT",
                        _display_path(log_path, vault_root),
                        f"{line_number}행의 작업 기록 형식을 확인하세요: {line}",
                    )
                )

    return AuditResult(tuple(issues), len(wiki_files), len(raw_files), total_links)


def _print_issues(issues: Iterable[Issue]) -> None:
    for issue in sorted(issues, key=lambda item: (item.severity, item.path, item.code)):
        print(f"[{issue.severity}] {issue.code} | {issue.path} | {issue.message}")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    default_vault = Path(__file__).resolve().parents[1] / "vault"
    vault_root = Path(argv[0]) if argv else default_vault
    result = audit_vault(vault_root)

    print("LLM Wiki 점검 결과")
    print(f"- Wiki 문서: {result.wiki_pages}")
    print(f"- Raw 원문: {result.raw_sources}")
    print(f"- Wikilink: {result.wikilinks}")
    print(f"- 오류: {len(result.errors)}")
    print(f"- 경고: {len(result.warnings)}")

    if result.issues:
        print()
        _print_issues(result.issues)

    if result.errors:
        print("\nFAIL: 오류를 먼저 수정하세요.")
        return 1

    print("\nPASS: 기본 형식과 연결 상태가 정상입니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

