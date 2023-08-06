# 1€ filter typescript version

Provides a typescript implementation for the [1€ filter](https://gery.casiez.net/1euro/).

## Install

```npm install 1eurofilter```

## Minimal example

```
import {OneEuroFilter} from '1eurofilter'

let frequency = 120; // Hz
let mincutoff = 1.0; // Hz
let beta = 0.1;      
let dcutoff = 1.0; 

let f = new OneEuroFilter(frequency, mincutoff, beta, dcutoff);

let noisyvalue = 2.1;
let timestamp = 0.0; // in seconds

let filtered = f.filter(noisyvalue, timestamp);

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

