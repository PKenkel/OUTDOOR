========
Overview
========

OUTDOOR ( Open Superstructure Modeling and Optimization Framework) is a tool to construct superstructure optimization models and solve them using MILP solvers. 
 
The Program consists of three main aspects:

1) The outdoor_core module provides classes for unit operations such as Reactors and stream splitters, as well as a class for system data like electricity prices and heating utilities. These Classes can be used to construct superstructures by creating unit operations objects and adding them to a superstructure class object. 

2) The outdoor_core module also implements a generic MILP superstructure model, which is written as an PYOMO abstract model, and can be applied to different cases such as biorefineries, chemical industry or Power-to-X. The generic model is created and afterwards converted into a concrete model by initializing the data from the populated superstructure.

3) Objects and data can either be created and populated by python scripting utilizing class-specific setter function. However, outdoor also includes a excel_wrapper tool which turn predesigned excel templates automatically into populated superstructures which can be solved using the outdoor framework. 

An example is proved in the example folder.



.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/OUTDOOR/badge/?style=flat
    :target: https://readthedocs.org/projects/OUTDOOR
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/PKenkel/OUTDOOR.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/PKenkel/OUTDOOR

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/PKenkel/OUTDOOR?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/PKenkel/OUTDOOR

.. |requires| image:: https://requires.io/github/PKenkel/OUTDOOR/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/PKenkel/OUTDOOR/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/PKenkel/OUTDOOR/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/PKenkel/OUTDOOR

.. |version| image:: https://img.shields.io/pypi/v/outdoor.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/outdoor

.. |wheel| image:: https://img.shields.io/pypi/wheel/outdoor.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/outdoor

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/outdoor.svg
    :alt: Supported versions
    :target: https://pypi.org/project/outdoor

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/outdoor.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/outdoor

.. |commits-since| image:: https://img.shields.io/github/commits-since/PKenkel/OUTDOOR/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/PKenkel/OUTDOOR/compare/v0.0.0...master



.. end-badges

SHORT DESCRIPTION

* Free software: MIT license

Installation
============

::

    pip install outdoor

You can also install the in-development version with::

    pip install https://github.com/PKenkel/OUTDOOR/archive/master.zip


Documentation
=============


https://outdoor.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
