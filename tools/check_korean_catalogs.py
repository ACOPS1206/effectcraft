#!/usr/bin/env python3
"""Check Korean catalog coverage and string invariants without a Rust toolchain.

This is a source-data check, not a substitute for cargo tests or UI review.
Run from any directory: python3 tools/check_korean_catalogs.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "crates/ui-egui/src"
STRING = r'"(?:[^"\\]|\\.)*"'


def rows(text, width):
    pattern = r'\(\s*' + STRING + (r'\s*,\s*' + STRING) * (width - 1) + r'\s*,?\s*\)'
    return [tuple(json.loads(value) for value in re.findall(STRING, row)) for row in re.findall(pattern, text)]


def table(path, name, width):
    text = path.read_text(encoding="utf-8").split("const " + name + ":", 1)[1]
    return rows(text.split("= &[", 1)[1].split("\n];", 1)[0], width)


def main():
    menus = table(SRC / "i18n/korean_menus.rs", "KOREAN", 3)
    panels = table(SRC / "i18n/korean_ui.rs", "KOREAN", 2)
    effects = table(SRC / "i18n/korean_effects.rs", "KOREAN", 3)
    categories = table(SRC / "i18n/korean_effects.rs", "KOREAN_CATEGORIES", 2)
    for label, catalog in [("menus", menus), ("panels", panels), ("effects", effects), ("categories", categories)]:
        keys = [row[:-1] for row in catalog]
        assert len(keys) == len(set(keys)), f"{label}: duplicate keys"
        for row in catalog:
            source, translated = row[-2:]
            assert translated.strip(), f"{label}: empty translation: {source}"
            assert source.count("{}") == translated.count("{}"), f"{label}: placeholders: {source}"
            assert source.count("\n") == translated.count("\n"), f"{label}: line breaks: {source}"
            assert source.count("...") == translated.count("..."), f"{label}: dialog ellipsis: {source}"
        print(f"{label}: {len(catalog)} rows OK")
    reference = table(SRC / "i18n.rs", "FRENCH", 3)
    assert {row[:2] for row in menus} == {row[:2] for row in reference}, "menu coverage differs"
    for _, source, translated in menus:
        assert sum(source.count(c) for c in "()") == sum(translated.count(c) for c in "()"), source
    for constant, korean, width in [("FRENCH", effects, 3), ("FRENCH_CATEGORIES", categories, 2)]:
        reference = table(SRC / "i18n/effects.rs", constant, width)
        assert {row[:-1] for row in korean} == {row[:-1] for row in reference}, constant
    source = (SRC / "i18n/ui.rs").read_text(encoding="utf-8")
    sources = set()
    for body in re.findall(r'const \w+: &\[\(&str, &str\)\] = &\[(.*?)\n\];', source, re.S):
        sources.update(row[0] for row in rows(body, 2))
    assert sources <= {row[0] for row in panels}, "panel catalog sources missing"
    preferences = (ROOT / "crates/engine/src/settings/prefs/choices.rs").read_text(encoding="utf-8")
    registry = table(ROOT / "crates/engine/src/settings/prefs/choices.rs", "LANGUAGES", 2)
    codes = [code for _, code in registry if code not in ("system", "en")]
    listed = re.search(r'const CATALOG_CODES:.*?= \[(.*?)\];', (SRC / "i18n.rs").read_text(), re.S)
    assert listed is not None
    assert codes == [json.loads(v) for v in re.findall(STRING, listed.group(1))], "language order mismatch"
    assert '("한국어", "ko")' in preferences
    assert dict(panels)["Light"] == "라이트", "appearance light mode is not a light source"
    print(f"PASS: {sum(map(len, (menus, panels, effects, categories)))} rows; coverage, IDs and placeholders preserved")


if __name__ == "__main__":
    main()
