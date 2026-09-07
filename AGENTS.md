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

**Обов’язок:** для **кожного** релізу (tag `vX.Y.Z` / GitHub Release) генерувати файл **`RELEASE_NOTES.md`** у корені репозиторію і **публікувати його разом із релізом**.

### 3.1. Коли створювати

- Перед створенням git tag і публікацією GitHub Release.
- Вміст базується на секції відповідної версії в `CHANGELOG.md` (Added / Changed / Fixed / Removed).
- Файл **перезаписується** під кожен новий реліз (історія — у `CHANGELOG.md` і в тілах минулих GitHub Releases).

### 3.2. Зміст і формат

Мінімальний шаблон:

```markdown
# FortiDebug Builder X.Y.Z

**Дата:** YYYY-MM-DD  
**Tag:** vX.Y.Z

## Highlights
- …

## Added
- …

## Changed
- …

## Fixed
- …

## Install
- Windows EXE: вкладення `FortiDebugBuilder.exe` у цьому Release
- З вихідників: `pip install -r requirements.txt && python src/main.py`

## Full changelog
Див. [CHANGELOG.md](CHANGELOG.md).
```

Мова: українська (як CHANGELOG) або змішана UK/EN — узгоджено з тоном репозиторію.

### 3.3. Публікація разом із релізом

1. Закомітити `RELEASE_NOTES.md` **до** `git tag` / створення Release.
2. Створити GitHub Release для tag `vX.Y.Z`.
3. CI (`.github/workflows/build-windows.yml`) при `release: published`:
   - збирає `FortiDebugBuilder.exe`;
   - прикріплює EXE **і** `RELEASE_NOTES.md` до Release;
   - підставляє тіло Release з `RELEASE_NOTES.md` (`body_path`), якщо файл є в checkout.

Ручний fallback: завантажити `RELEASE_NOTES.md` як asset і вставити текст у Description Release.

### 3.4. Чеклист перед tag

- [ ] `CHANGELOG.md` — секція `[X.Y.Z]` заповнена, `[Unreleased]` очищено або перенесено
- [ ] `RELEASE_NOTES.md` згенеровано з цієї секції
- [ ] Версія в `src/ui/tabs/about.py` (`APP_VERSION`) і README узгоджені
- [ ] `doc/INDEX.md` актуальний (якщо змінювались плани)
- [ ] Коміт(и) з нотатками **перед** `git tag vX.Y.Z && git push origin vX.Y.Z`

---

## 4. Короткий порядок релізу

```text
1. План у doc/ (якщо не тривіальний patch)
2. Код + тести + «не зламай!»
3. CHANGELOG [X.Y.Z]
4. RELEASE_NOTES.md
5. about.py / README version bump
6. Commit & push
7. git tag vX.Y.Z && git push origin vX.Y.Z
8. GitHub Release (published) → CI прикріплює EXE + RELEASE_NOTES.md
```

---

*Оновлено: 2026-09-07 — додано §3 RELEASE_NOTES.md.*
