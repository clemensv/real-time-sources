# Notebook Substitution Table

Apply each substitution exactly. The template file is
`pegelonline/notebook/pegelonline-feed.ipynb`.

## Required substitutions

Let:

- `$SOURCE` = source id (e.g. `bafu-hydro`).
- `$DISPLAY` = display name from `catalog.json` `name` field
  (e.g. `BAFU Hydro`).
- `$PKG` = the Python import package, taken from `pyproject.toml`
  `[tool.poetry] name` (after `-` → `_`).
- `$MODULE` = the bridge module file stem (e.g. `bafu_hydro`,
  `pegelonline`).
- `$ARGV0` = the bridge CLI name (usually equals `$SOURCE`, but check
  `pyproject.toml [tool.poetry.scripts]` for the script entry).
- `$SUBCOMMAND` = the bridge subcommand for live feed (`feed` in most
  bridges; check argparse setup).

| Cell | From | To |
|---|---|---|
| 1 (markdown) | `# Pegelonline Feeder (Fabric Notebook)` | `# $DISPLAY Feeder (Fabric Notebook)` |
| 1 (markdown) | `Polls the German WSV PegelOnline API ...` (paragraph) | One adapted paragraph from `$SOURCE/README.md`. Keep the bullet list structure. |
| 1 (markdown) | `` `pegelonline` package `` | `` `$PKG` package `` |
| 1 (markdown) | `pegelonline feed --once` | `$ARGV0 $SUBCOMMAND --once` |
| 2 (params) | `EVENTSTREAM_NAME = "pegelonline-ingest"` | `EVENTSTREAM_NAME = "$SOURCE-ingest"` |
| 2 (params) | `STATE_FILE       = "/lakehouse/default/Files/feeder-state/pegelonline/state.json"` | `STATE_FILE       = "/lakehouse/default/Files/feeder-state/$SOURCE/state.json"` |
| 4 (run) | `LOG_PATH = '/lakehouse/default/Files/feeder-state/pegelonline/last-run.log'` | `LOG_PATH = '/lakehouse/default/Files/feeder-state/$SOURCE/last-run.log'` |
| 4 (run) | `from pegelonline import pegelonline as feeder` | `from $PKG import $MODULE as feeder` |
| 4 (run) | `sys.argv = ['pegelonline', 'feed', '--once'] if ONCE_MODE else ['pegelonline', 'feed']` | `sys.argv = ['$ARGV0', '$SUBCOMMAND', '--once'] if ONCE_MODE else ['$ARGV0', '$SUBCOMMAND']` |

## Do NOT change

- The `_get_pbi_token`, `_resolve_workspace_id`,
  `lookup_es_connection_string` functions in cell 3. They are
  source-agnostic and load-bearing.
- The worker-thread wrapper in cell 4.
- The `notebookutils.notebook.exit("OK" | "FAIL: ...")` calls.
- The `try/except` envelope around the entire run cell.
- The cell ordering or the `parameters` tag on cell 2.

## Variant: bridge with no subcommand

If `$MODULE.main()` is invoked without a subcommand (uncommon — check
the bridge's argparse), use:

```python
sys.argv = ['$ARGV0', '--once'] if ONCE_MODE else ['$ARGV0']
```

## Variant: bridge that reads `ONCE_MODE` env var instead of `--once`

A few bridges (e.g. `gdacs`) honor an `ONCE_MODE` env var directly
rather than a CLI flag. In that case:

```python
os.environ['ONCE_MODE'] = 'true' if ONCE_MODE else 'false'
sys.argv = ['$ARGV0']
```

The deploy script already sets `ONCE_MODE` env in the params cell, so
this works.

## Anti-patterns (immediate abort)

- The bridge calls `asyncio.run(main_async())` but has no `--once` or
  `ONCE_MODE` exit path. Adding one means re-architecting the polling
  loop — out of scope.
- The bridge opens a websocket/MQTT/SSE connection. The notebook
  hosting pattern does not support long-lived connections; the deploy
  script's scheduler expects single-cycle exits.
- The bridge has no `def main():` entry point or uses an unusual
  invocation pattern (e.g. only callable via `python -m`). Adapt only
  if `python -m $PKG.$MODULE` works with `sys.argv` injection.
