# 1€ filter

Provides a python implementation for the [1€ filter](https://gery.casiez.net/1euro/).


## Install
```pip install OneEuroFilter --upgrade```

## Minimal example

```
from OneEuroFilter import OneEuroFilter

config = {
    'freq': 120,       # Hz
    'mincutoff': 1.0,  # Hz
    'beta': 0.1,       
    'dcutoff': 1.0    
    }

f = OneEuroFilter(**config)

# First parameter is the value to filter
# the second parameter is the current timestamp in seconds
filtered = f(2.1, 0)

```

## Related publication

[![DOI](https://img.shields.io/badge/doi-10.1145%2F2207676.2208639-blue)](https://doi.org/10.1145/2207676.2208639)

```
@inproceedings{10.1145/2207676.2208639,
author = {Casiez, G\'{e}ry and Roussel, Nicolas and Vogel, Daniel},
title = {1 € Filter: A Simple Speed-Based Low-Pass Filter for Noisy Input in Interactive Systems},
year = {2012},
isbn = {9781450310154},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/2207676.2208639},
doi = {10.1145/2207676.2208639},
pages = {2527–2530},
numpages = {4},
keywords = {noise, jitter, lag, precision, filtering, responsiveness, signal},
location = {Austin, Texas, USA},
series = {CHI '12}
}
```


