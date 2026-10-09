"""
Public-API conformance tests for sdypy-FRF.

``sdypy.FRF`` is a curated re-export of pyFRF, so the SEP 2 names it exposes
are decided by pyFRF's signatures.  These tests pin that contract at the
wrapper, mirroring ``tests/test_public_api_conformance.py`` in sdypy-EMA:

  (a) every entry in sdypy.FRF.__all__ resolves via getattr
  (b) no leaked third-party or stdlib names in sdypy.FRF.__all__
  (c) sdypy.FRF.FRF is the pyFRF.FRF class itself, not a copy
  (d) FRF(frf_estimator=...) and get_FRF(frf_estimator=..., frf_form=...)
      run without DeprecationWarning; positional and keyword calls agree
  (e) FRF(frf_type=...) emits DeprecationWarning and behaves as frf_estimator
  (f) get_FRF(type=..., form=...) emits DeprecationWarning and returns the
      same result as get_FRF(frf_estimator=..., frf_form=...)
"""

import warnings

import numpy as np
import pytest
import pyFRF

import sdypy.FRF as FRF

FS = 1000
N_SAMPLES = 2000


@pytest.fixture(scope="module")
def signals():
    rng = np.random.default_rng(0)
    return rng.standard_normal(N_SAMPLES), rng.standard_normal(N_SAMPLES)


def _frf(signals, **kwargs):
    exc, resp = signals
    return FRF.FRF(sampling_freq=FS, exc=exc, resp=resp,
                   exc_type='f', resp_type='a', **kwargs)


def _deprecation_messages(records):
    return [str(r.message) for r in records
            if issubclass(r.category, DeprecationWarning)]


# ---------------------------------------------------------------------------
# (a), (b), (c) curated surface
# ---------------------------------------------------------------------------

def test_all_entries_resolvable():
    assert FRF.__all__, "sdypy.FRF.__all__ must be non-empty"
    for name in FRF.__all__:
        assert hasattr(FRF, name), f"sdypy.FRF.{name} listed in __all__ but not found"
        assert getattr(FRF, name) is not None


def test_leaked_names_not_in_all():
    for name in ("np", "numpy", "scipy", "warnings", "pyFRF"):
        assert name not in FRF.__all__, f"{name!r} must not appear in sdypy.FRF.__all__"


def test_frf_class_is_pyfrf_class():
    assert FRF.FRF is pyFRF.FRF


# ---------------------------------------------------------------------------
# (d) canonical names: no warning, positional == keyword
# ---------------------------------------------------------------------------

def test_canonical_names_no_deprecation_warning(signals):
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        obj = _frf(signals, frf_estimator='H1')
        by_keyword = obj.get_FRF(frf_estimator='H1', frf_form='receptance')
        by_position = obj.get_FRF('H1', 'receptance')
    assert obj.frf_estimator == 'H1'
    np.testing.assert_array_equal(by_keyword, by_position)


# ---------------------------------------------------------------------------
# (e) deprecated frf_type constructor kwarg
# ---------------------------------------------------------------------------

def test_frf_type_emits_deprecation_warning_and_matches(signals):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        old = _frf(signals, frf_type='H2')
    messages = _deprecation_messages(w)
    assert messages, "FRF(frf_type=...) must emit DeprecationWarning"
    assert any("frf_estimator" in m for m in messages)

    new = _frf(signals, frf_estimator='H2')
    assert old.frf_estimator == new.frf_estimator == 'H2'
    np.testing.assert_array_equal(old.get_FRF(), new.get_FRF())


# ---------------------------------------------------------------------------
# (f) deprecated type / form kwargs of get_FRF
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("estimator", ['H1', 'H2', 'Hv'])
@pytest.mark.parametrize("form", ['receptance', 'mobility', 'accelerance'])
def test_get_frf_type_form_emit_deprecation_warning_and_match(signals, estimator, form):
    obj = _frf(signals)
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        reference = obj.get_FRF(frf_estimator=estimator, frf_form=form)

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        old = obj.get_FRF(type=estimator, form=form)
    messages = _deprecation_messages(w)
    assert any("frf_estimator" in m for m in messages), "type= must point at frf_estimator"
    assert any("frf_form" in m for m in messages), "form= must point at frf_form"
    np.testing.assert_array_equal(old, reference)
