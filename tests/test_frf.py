# -*- coding: utf-8 -*-
"""
Functional tests for sdypy.FRF (backed by pyFRF).

Test coverage
-------------
1. test_h1_peak_frequency
   Synthesise a noise-free SDOF impulse response.  Instantiate FRF with
   exc (unit impulse) and resp (damped sinusoid), call get_H1() and
   assert that the magnitude peak is within one frequency bin of the true
   natural frequency.

2. test_get_f_axis_length_and_spacing
   Assert that get_f_axis() returns the expected number of points
   (rfft length = fft_len//2 + 1) and that the spacing between
   consecutive frequency bins equals fs/fft_len.

3. test_assert_sep005_valid_accepted
   A fully compliant SEP-005 dict (data=np.ndarray, name, unit_str, fs)
   is passed to sdypy.FRF.assert_sep005; assert no exception is raised.

4. test_assert_sep005_invalid_raises
   A dict missing the compulsory 'name' key is rejected.  assert_sep005
   raises ValueError (the real behaviour — it never returns False).
"""

import numpy as np
import pytest

import sdypy.FRF as FRF_module
from sdypy.FRF import FRF, assert_sep005


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _sdof_signals(f_n=50.0, zeta=0.02, fs=2000, duration=2.0):
    """
    Return (exc, resp) 1-D arrays for a noise-free SDOF system.

    exc  : unit impulse at t=0
    resp : x(t) = (1/wd) * exp(-zeta*wn*t) * sin(wd*t)
           (impulse response of a unit-mass, undamped natural freq f_n)
    """
    n = int(fs * duration)
    t = np.arange(n) / fs

    exc = np.zeros(n)
    exc[0] = 1.0          # unit impulse

    wn = 2.0 * np.pi * f_n
    wd = wn * np.sqrt(1.0 - zeta ** 2)
    resp = (1.0 / wd) * np.exp(-zeta * wn * t) * np.sin(wd * t)

    return exc, resp


# ---------------------------------------------------------------------------
# test 1 — H1 peak frequency sanity
# ---------------------------------------------------------------------------

def test_h1_peak_frequency():
    """H1 magnitude peak must be within one frequency bin of f_n."""
    fs = 2000
    f_n = 50.0
    duration = 2.0

    exc, resp = _sdof_signals(f_n=f_n, zeta=0.02, fs=fs, duration=duration)

    frf_obj = FRF(
        sampling_freq=fs,
        exc=exc,
        resp=resp,
        exc_type='f',
        resp_type='a',
        frf_type='H1',
    )

    # get_FRF(form='accelerance') returns the H1 accelerance estimator.
    # DC bin (index 0) is NaN due to the 1/w^2 -> w^2 round-trip at w=0;
    # skip it when locating the magnitude peak.
    h1_acc = frf_obj.get_FRF(type='H1', form='accelerance')
    f_axis = frf_obj.get_f_axis()   # Hz

    # squeeze to 1-D magnitude, exclude DC
    h1_mag = np.abs(h1_acc[0, 0, 1:])
    f_noDC = f_axis[1:]

    peak_idx = np.argmax(h1_mag)
    f_peak = f_noDC[peak_idx]

    df = f_axis[1] - f_axis[0]      # frequency bin width

    assert abs(f_peak - f_n) <= df, (
        f"H1 peak at {f_peak:.3f} Hz is more than one bin ({df:.3f} Hz) "
        f"away from the true natural frequency {f_n} Hz"
    )


# ---------------------------------------------------------------------------
# test 2 — get_f_axis length and spacing
# ---------------------------------------------------------------------------

def test_get_f_axis_length_and_spacing():
    """
    get_f_axis() must return fft_len//2 + 1 points with uniform spacing
    fs/fft_len Hz between bins.
    """
    fs = 1000
    n_samples = 512          # number of time samples
    fft_len = 512            # explicit fft length == data length

    exc = np.ones(n_samples)
    resp = np.ones(n_samples)

    frf_obj = FRF(
        sampling_freq=fs,
        exc=exc,
        resp=resp,
        exc_type='f',
        resp_type='a',
        fft_len=fft_len,
    )

    f = frf_obj.get_f_axis()

    expected_len = fft_len // 2 + 1
    assert len(f) == expected_len, (
        f"Expected {expected_len} frequency points, got {len(f)}"
    )

    expected_df = fs / fft_len
    actual_df = f[1] - f[0]
    assert abs(actual_df - expected_df) < 1e-10, (
        f"Expected df={expected_df} Hz, got {actual_df} Hz"
    )

    # all spacings are uniform
    diffs = np.diff(f)
    assert np.allclose(diffs, diffs[0], atol=1e-10), (
        "get_f_axis() does not return uniformly spaced frequencies"
    )


# ---------------------------------------------------------------------------
# test 3 — assert_sep005 accepts a valid dict
# ---------------------------------------------------------------------------

def test_assert_sep005_valid_accepted():
    """A fully compliant SEP-005 dict must not raise."""
    valid = {
        'data': np.array([1.0, 2.0, 3.0]),
        'name': 'acceleration channel 1',
        'unit_str': 'm/s^2',
        'fs': 1000,
    }
    # must not raise any exception
    assert_sep005(valid)


# ---------------------------------------------------------------------------
# test 4 — assert_sep005 raises on invalid dict
# ---------------------------------------------------------------------------

def test_assert_sep005_invalid_raises():
    """
    assert_sep005 raises ValueError when a compulsory key is absent.

    Implementation note: assert_sep005 always raises — it never returns
    False.  Missing 'name' triggers ValueError("Missing compulsory
    keyword 'name'").
    """
    invalid = {
        # 'name' is intentionally omitted
        'data': np.array([1.0, 2.0, 3.0]),
        'unit_str': 'm/s^2',
        'fs': 1000,
    }
    with pytest.raises(ValueError, match="Missing compulsory keyword 'name'"):
        assert_sep005(invalid)
