# AGENTS.md — обов’язкові правила для агентів і розробників

**Проект:** FortiDebug Builder (Windows)  
**Репозиторій:** usednetua/project-FortiDebug

Цей файл — джерело правил процесу. Порушення не допускається без явної згоди власника.

---

## 1. CHANGELOG перед комітом

**Завжди** записуй зміни в `CHANGELOG.md` **перед** комітом (розділ `[Unreleased]` або відповідна версія).

---

## 2. Кодекс впровадження

Обов’язково дотримуйся [doc/CODEX_IMPLEMENTATION.md](doc/CODEX_IMPLEMENTATION.md):

1. Перед початком впровадження будь-чого — детальний покроковий план у файлі в папці `doc/`.
2. На початку плану — таблиця зі всіма етапами, станом виконання та примітками.
3. Після кожного етапу — перевірка всього зачепленого функціоналу та сумісності з уже робочими частинами (принцип **«не зламай!»**).

При створенні, зміні або видаленні будь-якого файлу в `doc/` обов’язково актуалізуй [doc/INDEX.md](doc/INDEX.md) (той самий коміт або безпосередньо перед ним).

---

## 3. RELEASE_NOTES.md під кожен реліз

**Обов’язок:** для **кожного** релізу (tag `vX.Y.Z` / GitHub Release) мати **`RELEASE_NOTES.md`** у корені репозиторію і **публікувати його разом із релізом**.

### 3.1. Автогенерація (обов’язковий інструмент)

Джерело правди — `CHANGELOG.md`. Нотатки **генеруються** скриптом:

```bash
# остання версійна секція
python scripts/generate_release_notes.py

# конкретна версія
python scripts/generate_release_notes.py 0.19.0
python scripts/generate_release_notes.py v0.19.0 --tag v0.19.0

# перевірка наявності секції (CI / pre-tag)
python scripts/generate_release_notes.py 0.19.0 --check
```

Скрипт читає `## [X.Y.Z] — YYYY-MM-DD`, секції Added/Changed/Fixed/… і пише `RELEASE_NOTES.md` (Highlights + Install + посилання на CHANGELOG).

**CI** (`.github/workflows/build-windows.yml`) при `release: published`:
1. Бере версію з `github.event.release.tag_name` (`v0.19.0` → `0.19.0`).
2. Запускає `python scripts/generate_release_notes.py <ver> --tag <tag>`.
3. Прикріплює EXE + `RELEASE_NOTES.md` і ставить body Release з `body_path: RELEASE_NOTES.md`.

Тобто навіть якщо файл у гілці застарів, **опублікований Release завжди отримає свіжі нотатки з CHANGELOG на момент tag/checkout**.

Рекомендовано також згенерувати і закомітити `RELEASE_NOTES.md` **перед** tag (для читабельності в `main`), але для публікації достатньо коректної секції в CHANGELOG.

### 3.2. Коли готувати CHANGELOG

- Перед tag: перенести пункти з `[Unreleased]` у `## [X.Y.Z] — YYYY-MM-DD`.
- Не публікувати Release, поки `python scripts/generate_release_notes.py X.Y.Z --check` не поверне 0.

### 3.3. Чеклист перед tag

- [ ] `CHANGELOG.md` — секція `[X.Y.Z]` заповнена
- [ ] `python scripts/generate_release_notes.py X.Y.Z` (або покластися на CI)
- [ ] Версія в `src/ui/tabs/about.py` (`APP_VERSION`) і README узгоджені
- [ ] `doc/INDEX.md` актуальний (якщо змінювались плани)
- [ ] Commit & push → `git tag vX.Y.Z && git push origin vX.Y.Z` → Publish Release

---

## 4. Короткий порядок релізу

```text
1. План у doc/ (якщо не тривіальний patch)
2. Код + тести + «не зламай!»
3. CHANGELOG [X.Y.Z] (з [Unreleased])
4. python scripts/generate_release_notes.py X.Y.Z   # опційно закомітити
5. about.py / README version bump
6. Commit & push
7. git tag vX.Y.Z && git push origin vX.Y.Z
8. GitHub Release (published) → CI: generate notes + EXE + attach + body
```

---

*Оновлено: 2026-09-07 — §3 автогенерація RELEASE_NOTES.md.*
