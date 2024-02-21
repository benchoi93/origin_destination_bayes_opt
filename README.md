# origin_destination_bayes_opt

Current directory contains the "v4" version of OD. This is used to test three different BO algorithms:
- Vanilla BO: https://botorch.org/tutorials/closed_loop_botorch_only
  - Notebook: `bayesian_optimization/01_bo_vanilla.ipynb`
- High-Dimensional sample-efficient Bayesian Optimization with SAASBO: https://botorch.org/tutorials/saasbo
  - Notebook: `bayesian_optimization/02_bo_highdim.ipynb`
- Trust Region BO: https://botorch.org/tutorials/turbo_1
  - Notebook: `bayesian_optimization/03_bo_trust_region.ipynb`


## Testing

If you want to test a single run of simulator use the notebook `bayesian_optimization/00_test_simulator.ipynb`

## Helpers

All helper functions that are used to run simulations are saved in `bayesian_optimization/helpers.py`. These functions were refactored from `generate_routes.ipynb`.

## Git ignore
The following files need to be added into the root folder of this repo in order to run simulations. These are part of gitignore in order to make the repo light weight:
- `SFO.net.xml`
- `5hr_*`
- `additional*`