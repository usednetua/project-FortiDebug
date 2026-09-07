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

---

## Детальні кроки

### 1. AGENTS.md
Повний текст правил агента в репозиторії: CHANGELOG, CODEX, **RELEASE_NOTES під кожен реліз + публікація з Release**.

### 2. CODEX
Додати рядок у таблицю «Зв’язок з іншими правилами».

### 3. CI
`softprops/action-gh-release`:
- `files:` EXE + `RELEASE_NOTES.md`
- `body_path: RELEASE_NOTES.md` (тіло GitHub Release)
- не падати, якщо нотаток немає лише на старих tag без файлу — для нових релізів файл обов’язковий за AGENTS.

### 4. Приклад
`RELEASE_NOTES.md` у корені для **0.18.2** (scrollable dropdowns + посилання на UX 0.18.1).

---

*Оновлено: 2026-09-07*
