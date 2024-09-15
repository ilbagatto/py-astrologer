# Astrologer

- [Astrologer](#astrologer)
  - [Features](#features)
  - [Installation](#installation)
    - [Virtual environment](#virtual-environment)
    - [Install the package](#install-the-package)
  - [Usage](#usage)
  - [Unit tests](#unit-tests)


Calculations for traditional Western astrology.

## Features


* Astrological houses using a wide range of systems.
* Sensitive points.
* Aspects and stelliums.
* A wide range of charts [TBD]. 


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
