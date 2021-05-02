# Package OMIEData: Open source tool for Electricity data analysis
Package to download electricity time series (prices and demand) from https://www.omie.es/

[![Build Status][build-button]][build]
[![Latest Version][mdversion-button]][md-pypi]
[![Python Versions][pyversion-button]][md-pypi]


[build-button]: https://github.com/acruzgarcia/OMIEData/actions?query=workflow/CI/badge.svg?event=push
[build]: https://github.com/acruzgarcia/OMIEData/actions?query=workflow/CI/badge.svg?event=push
[mdversion-button]: https://img.shields.io/pypi/v/Markdown.svg
[md-pypi]: https://pypi.org/project/OMIEData/
[pyversion-button]: https://img.shields.io/pypi/pyversions/Markdown.svg


## Installation 

The package is uploaded at https://pypi.org/project/OMIEData/0.0.1/, so the usual

```python
python -m pip install OMIEData

```
from the command line should work. 

Aternatively, to install it from GitHub, type:

```python
python -m pip install git+https://github.com/acruzgarcia/OMIEData

```

or use the .whl (or .tar.gz) file within dist folder:

```python
python -m pip install OMIEData-0.0.1-py3-none-any.whl

```
or

```python
python -m pip install OMIEData-0.0.1.tar.gz

```

# Use case examples:
Files 'example_energy_by_technology.py' and 'example_marginal_price.py' illustrates the use of the package. Enjoy!.
