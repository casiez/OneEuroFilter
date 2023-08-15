[![Tests](https://github.com/casiez/OneEuroFilter/actions/workflows/tests.yml/badge.svg)](https://github.com/casiez/OneEuroFilter/actions/workflows/tests.yml)

# 1€ filter

Provides implementations for the [1€ filter](https://gery.casiez.net/1euro/)

The 1€ filter ("one Euro filter") is a simple algorithm to filter noisy signals for high precision and responsiveness. It uses a first order low-pass filter with an adaptive cutoff frequency: at low speeds, a low cutoff stabilizes the signal by reducing jitter, but as speed increases, the cutoff is increased to reduce lag. The algorithm is easy to implement, uses very few resources, and with two easily understood parameters, it is easy to tune. In a comparison with other filters, the 1€ filter has less lag using a reference amount of jitter reduction.

See more on the [1€ filter homepage](https://gery.casiez.net/1euro/) for details on how to tune the parameters and try the [on-line interactive version](https://gery.casiez.net/1euro/InteractiveDemo/).

## Want to contribute?

1. [Fork](https://github.com/casiez/OneEuroFilter/fork) the repo.
1. Create a folder with your implementation and add the files for your implementation.
1. Create a file that can be executed to output in a console the result of the filtering for the ground truth. See the existing files as examples. Create a Makefile to test your implementation (see the other examples).
1. Update [docker/Dokerfile](docker/Dokerfile) to install what could be missing to compile your code.
1. Update [Makefile](Makefile) to call your makefile.
1. Create a pool request.

## Ground truth data
[groundTruth.csv](groundTruth.csv) has been generated using [this version of the C++ implementation](https://github.com/casiez/OneEuroFilter/blob/56126d84fd9107b4a8942deb5785a854730f404c/cpp/OneEuroFilter.cc), with code in the main to generate random noisy data and filter it. ```groundTruth.csv``` is used to check other implementations.

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


