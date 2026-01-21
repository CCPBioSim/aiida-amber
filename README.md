# aiida-amber
| Category       | Badges |
|----------------|--------|
| **Build**      | [![Build Status](https://github.com/CCPBioSim/aiida-amber/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/CCPBioSim/aiida-amber/actions/workflows/ci.yml) |
| **Documentation** | [![Docs status](https://readthedocs.org/projects/aiida-amber/badge)](http://aiida-amber.readthedocs.io/) |
| **PyPI**       | ![PyPI - Status](https://img.shields.io/pypi/status/aiida-amber?logo=pypi&logoColor=white) [![PyPI version](https://badge.fury.io/py/aiida-amber.svg)](https://badge.fury.io/py/aiida-amber)  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiida-amber) ![PyPI - Total Downloads](https://img.shields.io/pepy/dt/aiida-amber?logo=pypi&logoColor=white&color=blue) ![PyPI - Monthly Downloads](https://img.shields.io/pypi/dm/aiida-amber?logo=pypi&logoColor=white&color=blue)|
| **Quality**    | [![Coverage Status](https://coveralls.io/repos/github/CCPBioSim/aiida-amber/badge.svg?branch=main)](https://coveralls.io/github/CCPBioSim/aiida-amber?branch=main) |

The Amber plugin for AiiDA aims to enable the capture and sharing of the full
provenance of data when parameterising and running molecular dynamics
simulations. This plugin is being developed as part of the Physical Sciences
Data Infrastructure programme to improve the practices around data within the
Physical Sciences remit area within the UK.

This package is currently a work in progress and we will be adding much more
complete functionality to this plugin in the coming months.

The design pattern we are aiming for is to simply allow researchers to capture
the full data provenance for their simulations by only switching on an AiiDA
conda environment, along with modifying your command lines very slightly.

This means that you should gain access to powerful FAIR data practices without
wholesale cultural or usage pattern shifts in your daily work.

## Documentation

See [here](https://aiida-amber.readthedocs.io/en/latest/) for documentation for users and developers.

## License

MIT

## Contact

- jas.kalayan@stfc.ac.uk
- james.gebbie@stfc.ac.uk
