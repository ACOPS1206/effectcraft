# Korean interface localization

Select **한국어** in Settings → General → Language, or use Match System with a Korean
locale such as `ko-KR` or `ko_KR.UTF-8`.

The catalogs contain 632 fixed menu rows, 1,187 panel/dialog strings, 308 effect names
and 21 effect categories at base `e71dd629c56c78a82959ee50c271da9209c55b80`.
Translations were drafted from the English source with AI assistance. They were not copied
from the catalogs in earlier Korean PRs #1419, #1529 or #2000. Those independent efforts
predate this contribution and overlap its menu/panel scope.

Command IDs, effect IDs, property paths and project data remain unchanged. User-provided
file, layer, composition and workspace names stay verbatim. Effect search accepts both
the English and Korean names.

## Fonts and remaining work

The desktop interface uses installed fonts, including Apple SD Gothic Neo, Malgun Gothic,
Noto Sans CJK KR or Noto Sans KR when available. No new font asset is bundled. Catalog
characters are included in the existing additional-fallback coverage check.

The web build has no bundled Korean face. Match System skips Korean there, as it does
other unsupported scripts; explicitly selecting Korean still selects its catalog.

Effect parameter names, engine-generated properties/errors/history entries, tutorial
bodies and uncatalogued literals can still appear in English. The General settings option
`Scrub Composition Frames with Mouse Wheel` is one such remaining English label.

## Terminology

| English | Korean |
|---|---|
| Composition | 컴포지션 |
| Footage | 푸티지 |
| Anchor Point | 기준점 |
| Scale | 비율 |
| Keyframe | 키프레임 |
| Expression | 표현식 |
| Track Matte | 트랙 매트 |
| Pre-compose | 사전 구성 |
| Pick whip | 연결 도구 |
| Render Queue | 렌더링 대기열 |

## Validation

On Linux with Rust 1.95.0:

- `cargo fmt --all -- --check`: passed.
- `cargo test -p effectcraft-ui-egui --lib i18n -- --nocapture`: 43 passed; Korean
  missing-translations report: 0 for the sources the report tracks.
- `python3 tools/check_korean_catalogs.py`: 2,148 rows checked for coverage,
  duplicate keys, placeholders, line breaks and dialog ellipses.
- Headless UI snapshot example built and rendered the empty workspace and General settings;
  Korean glyphs were inspected with Noto CJK installed.
- macOS/Windows runtime rendering and native-speaker terminology review remain pending.

Initial parallel builds hit dependency archive/linker errors. A fresh target directory with
`CARGO_BUILD_JOBS=2 CARGO_INCREMENTAL=0 CARGO_PROFILE_DEV_CODEGEN_UNITS=1
CARGO_PROFILE_TEST_CODEGEN_UNITS=1` successfully built the UI crate and ran its i18n tests.
The full workspace gate status is recorded in the pull request rather than treated as a
successful local check here.
