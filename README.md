# cardiac-cells-py

> A playground for cardiac cell models, written in Python.

## Overview

This module provides a friendly interface to perform experiments on cardiac cells. The high level
interface is defined by the `CellModel` abstract base class and some common modelling experiments
are implemented in the `experiments` module. To run the experiments on a new cell model, all you
need to do is implement a new sub-class of CellModel.

The following models and cell types are currently available for use in the experiments:

- `minimal_model` (cell types: `endo`, `epi` and `m`):
Bueno-Orovio, A., Cherry, E. M., & Fenton, F. H. (2008). [Minimal model for human ventricular action potentials in tissue.](https://www.sciencedirect.com/science/article/pii/S0022519308001690?casa_token=QWCzx_CNyvAAAAAA:MiwwKVjy8kE3vt8uBffWYxCV39kt7Egh-7S8AmQ5eCl0VqFX98-sp3fYw6kSbcRn8uDuNInIIkU) Journal of theoretical biology, 253(3), 544-560.

## Install

To run experiments you will need to install the repo and its dependencies. We recommend that you
do so in a virtual environment. All functionality was last tested using Python3.9. The repo is
installed by cloning the code into your machine, navigating to `cardiac-cells-py` and doing:

```bash
pip install -e .
```

After which you should have all functionality available in your python environment.

## Running experiments

The above install will have installed in your virtual environment the `cell-experiments` command
line interface which you can use to run experiments with the available models. At the moment, the
following experiments are available:

- `steady-state`: stimulates the model for a fixed number of cycles and reports the action
potential shape, state variables and resulting currents.
- `ap-restitution`: performs an APD90 restitution experiment on the cell model and reports the
APD90 restitution curve.

## Type checks

The repo rellies on type checking to ensure that inputs and outputs of functions remain adequate as
the codebase evolves. If you would like to contribute to the repo, please ensure that you install
it with the mypy option:
```
pip install -e .[mypy]
```

and that you run type checks on the entire `cardiac-cells-py` repo before commiting your code:
```
mypy cardiac-cells-py --ignore-missing-imports
```