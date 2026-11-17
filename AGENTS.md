# AGENTS.md — sdypy-FRF contributor & agent guide

Guidance for anyone (human or AI) developing **sdypy-FRF**. Claude Code reads
it via a one-line `CLAUDE.md` (`@AGENTS.md`). The org-wide rules (development
workflow, SEP governance, naming, canonical specs) live in the sdypy hub and are
linked at the end, never restated here.

## What this package is

Frequency response functions: the `FRF` portion of the `sdypy` namespace (PEP
420, `from sdypy import FRF`). It estimates FRFs (H1, H2, Hv, ODS) from
excitation and response signals, with averaging and windowing. The code
(`sdypy/FRF/frf.py`, `sdypy/FRF/fft_tools.py`) came from pyFRF with its
history; pyFRF is now a thin port that imports from here. The public API is the
curated `__all__` in `sdypy/FRF/__init__.py`.

## Development environment

Use `uv`. Supported Python versions: `requires-python` in `pyproject.toml`.

```console
uv venv && uv pip install -e ".[dev]"   # dev install
pytest                                  # tests
python -m build                         # sdist + wheel
```

## Org-wide rules (sdypy hub)

Copied verbatim from the hub's `AGENTS.md`; edit it there. The hub's template
checker compares this copy.

<!-- >>> sdypy hub links -->
- [AGENTS.md](https://github.com/sdypy/sdypy/blob/main/AGENTS.md) — workflow and definition of done
- [AGENTS.md § Releasing](https://github.com/sdypy/sdypy/blob/main/AGENTS.md#releasing) — the only way to release
- [docs/seps/](https://github.com/sdypy/sdypy/tree/main/docs/seps/) — SEP governance docs
- [docs/source/dev/nomenclature.rst](https://github.com/sdypy/sdypy/blob/main/docs/source/dev/nomenclature.rst) — naming a new public term (SEP 2)
- [openspec/specs/](https://github.com/sdypy/sdypy/tree/main/openspec/specs/) — canonical capability specs
- [REQUIREMENTS.md](https://github.com/sdypy/sdypy/blob/main/REQUIREMENTS.md) — requirements roster
<!-- <<< sdypy hub links -->
