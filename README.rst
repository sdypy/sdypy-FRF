sdypy-FRF
=========

Frequency response function as used in structural dynamics.
-----------------------------------------------------------

The ``sdypy-FRF`` is a namespace project of the ``sdypy`` framework and is a direct link
to the ``pyFRF`` package.

Use the ``sdypy`` package to convieniently access the functionallity of the
`pyFRF <https://github.com/ladisk/pyFRF>`_ package through its namespace (see example below). 

Other functionalities of the ``sdypy`` framework include:

- `sdypy-EMA <https://github.com/sdypy/sdypy-EMA>`_: Experimental Modal Analysis
- `sdypy-io <https://github.com/sdypy/sdypy-io>`_: Input/Output operations (LVM files, UFF files)


For more information check out the showcase examples and see documentation_.

Basic ``sdypy-FRF`` usage:
--------------------------

Import the module:
~~~~~~~~~~~~~~~~~~~

.. code:: python

    from sdypy import FRF

Make an instance of ``FRF`` class:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    a = FRF.FRF(
        sampling_freq,
        exc=None,
        resp=None,
        exc_type='f', resp_type='a',
        window='none',
        weighting='linear',
        fft_len=None,
        nperseg=None,
        noverlap=None,
        archive_time_data=False,
        frf_type='H1',
        copy=True
    )

Adding data:
~~~~~~~~~~~~
We can add the excitation and response data at the beginning through ``exc`` and ``resp`` arguments, otherwise, the excitation and response 
data can be added later via ``add_data()`` method:

.. code:: python

    a.add_data(exc, resp)

Computing FRF:
~~~~~~~~~~~~~~
Preferable way to get the frequency response functions is via ``get_FRF()`` method:

.. code:: python

    frf = a.get_FRF(type="default", form="receptance")

We can also directly get the requested FRF via other methods: ``get_H1()``, ``get_H2()``, ``get_Hv()`` and, ``get_ods_frf()``:

.. code:: python

    H1 = a.get_H1()
    H2 = a.get_H2()
    Hv = a.get_Hv()
    ods_frf = a.get_ods_frf()

.. _documentation: https://pyfrf.readthedocs.io/en/latest/

|pytest|

|binder| to test the *Showcase.ipynb*.

.. |binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/ladisk/pyFRF/main
.. |pytest| image:: https://github.com/ladisk/pyFRF/actions/workflows/python-package.yml/badge.svg
    :target: https://github.com/ladisk/pyFRF/actions

