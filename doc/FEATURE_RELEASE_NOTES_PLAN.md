# FortiDebug Builder — обов’язок RELEASE_NOTES.md під кожен реліз

**Цільова версія процесу:** з 0.18.2+ / наступні релізи  
**Старт:** 2026-09-07

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 1 | Зафіксувати правило в AGENTS.md | ✅ Done | P0 | §3 RELEASE_NOTES |
| 2 | Оновити CODEX (зв’язок з правилами) | ✅ Done | P0 | секція 4 |
| 3 | CI: body_path + attach RELEASE_NOTES.md | ✅ Done | P0 | build-windows.yml |
| 4 | Згенерувати RELEASE_NOTES.md для 0.18.2 | ✅ Done | P1 | приклад / поточний |
| 5 | doc/INDEX.md | ✅ Done | P0 | |
| 6 | CHANGELOG [Unreleased] | ✅ Done | P0 | перед комітом |
| 7 | Regression: workflow YAML валідний | ✅ Done | P0 | «не зламай!» збірку EXE |
| 8 | **Автогенерація** `scripts/generate_release_notes.py` | ✅ Done | P0 | CHANGELOG → RELEASE_NOTES |
| 9 | CI step: generate from tag before attach | ✅ Done | P0 | version з tag_name |

---

## Детальні кроки

### Автогенерація

- Скрипт: `scripts/generate_release_notes.py` (stdlib only).
- Парсить `## [X.Y.Z] — YYYY-MM-DD` і `### Added|Changed|Fixed|…`.
- Пише `RELEASE_NOTES.md` з Highlights, категоріями, Install, посиланням на CHANGELOG.
- Відхиляє `[Unreleased]` як ціль публікації.
- CI на `release: published` завжди перегенеровує файл з checkout + tag.

### Локально

```bash
python scripts/generate_release_notes.py 0.19.0
python scripts/generate_release_notes.py 0.19.0 --check
```

---

*Оновлено: 2026-09-07 — автогенерація.*
