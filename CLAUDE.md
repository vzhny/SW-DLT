# CLAUDE.md

Fork of net00-1/SW-DLT (remote `upstream`). The shortcut runs a pinned copy of `src/SW_DLT.py` inside a-Shell on the phone.

## Commands

- Pin the shortcut to a script commit: `python3 tools/pin.py <commit>`. The commit must be pushed to `origin` first, because the phone downloads from raw.githubusercontent.com.
- Change the pip versions: edit `PINS` in `tools/pin.py`, then run it again.
- Sign: `cp src/SW-DLT.plist <tmp>/SW-DLT.shortcut && shortcuts sign --mode anyone --input <tmp>/SW-DLT.shortcut --output ~/Downloads/SW-DLT.shortcut`
- Check: `plutil -lint src/SW-DLT.plist`

## Architecture

- `src/SW-DLT.plist`: the shortcut. Edit it with `plistlib`: a load and dump round trip gives the same bytes, so diffs stay small. Text actions keep variables as U+FFFC characters, with their offsets in `attachmentsByRange`. If you change the text before a variable, update its offset.
- `src/SW_DLT.py`: the downloader. The shortcut runs it as `python SW_DLT.py '<url>' <args>`.

## Rules

- a-Shell parses `subprocess` command strings like a shell. Quote each value with `shlex.quote`.
- Each change to `src/SW_DLT.py` needs this order: commit, push, `tools/pin.py <commit>`, commit the plist, sign again. Phones that already have the script keep the old copy until you delete `~/Documents/SW-DLT/SW_DLT.py` in a-Shell or run the shortcut's uninstall setting.
- Do not commit signed `.shortcut` files.
