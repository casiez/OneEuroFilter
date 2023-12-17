[![PyPI Version](https://img.shields.io/pypi/v/OneEuroFilter)](https://pypi.org/project/OneEuroFilter/)
[![Downloads](https://static.pepy.tech/badge/OneEuroFilter)](https://pepy.tech/project/OneEuroFilter)

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

## Doc


### *class* OneEuroFilter.OneEuroFilter.OneEuroFilter(freq: float, mincutoff: float = 1.0, beta: float = 0.0, dcutoff: float = 1.0)

Bases: `object`

#### filter(x: float, timestamp: float = None)

Filters a noisy value.

* **Parameters:**
  * **x** (*float*) – Noisy value to filter.
  * **timestamp** (*float**,* *optional*) – timestamp in seconds.
* **Returns:**
  the filtered value
* **Return type:**
  float

#### reset()

Resets the internal state of the filter.

#### setBeta(beta: float)

Sets the Beta parameter.

* **Parameters:**
  **beta** (*float*) – Parameter to reduce latency (> 0).

#### setDerivateCutoff(dcutoff: float)

Sets the dcutoff parameter.

* **Parameters:**
  **dcutoff** (*float*) – Used to filter the derivates. 1 Hz by default. Change this parameter if you know what you are doing.

#### setFrequency(freq: float)

Sets the frequency of the input signal.

* **Parameters:**
  **freq** (*float*) – An estimate of the frequency in Hz of the signal (> 0), if timestamps are not available.
* **Raises:**
  **ValueError** – If one of the frequency is not >0

#### setMinCutoff(mincutoff: float)

Sets the filter min cutoff frequency.

* **Parameters:**
  **mincutoff** (*float*) – Min cutoff frequency in Hz (> 0). Lower values allow to remove more jitter.
* **Raises:**
  **ValueError** – If one of the frequency is not >0

#### setParameters(freq: float, mincutoff: float = 1.0, beta: float = 0.0, dcutoff=1.0)

Sets all the parameters of the filter.

* **Parameters:**
  * **freq** (*float*) – An estimate of the frequency in Hz of the signal (> 0), if timestamps are not available.
  * **mincutoff** (*float**,* *optional*) – Min cutoff frequency in Hz (> 0). Lower values allow to remove more jitter.
  * **beta** (*float**,* *optional*) – Parameter to reduce latency (> 0).
  * **dcutoff** (*float**,* *optional*) – Used to filter the derivates. 1 Hz by default. Change this parameter if you know what you are doing.
* **Raises:**
  **ValueError** – If one of the parameters is not >0

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


