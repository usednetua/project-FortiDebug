# Application icon

Generate `app.ico` (multi-size 16/32/48/256) without external deps:

```bash
# from repository root
python scripts/generate_icon.py
```

Output: `src/resources/icons/app.ico`

Then build EXE:

```bash
pyinstaller build.spec
```
