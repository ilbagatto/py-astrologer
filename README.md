# Astrologer

Library of core routines for practical astronomy aimed at astrological software and services.

## Features


* Astrological houses using a wide range of systems.
* Sensitive points.
* Aspects and stelliums.
* Builds a range of charts.


## Installation

### Virtual environment

Create virtual environment for Python3.12 or later and activate it.

On Linux:

```console
$ python3.12 -m venv .venv
$ . ./venv/bin/activate
```

For details see [Create and Use Virtual Environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments).


### Install the package

```console
$ pip install .
```

Or, for development mode:

```console
$ pip install -e '.[dev]'
```

## Usage

See tests/ and examples/ for usage examples.

## Unit tests

From the project root directory:

```console
$ pytest tests
```
