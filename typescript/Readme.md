[![NPM Version](https://badge.fury.io/js/1eurofilter.svg?style=flat)](https://npmjs.org/package/1eurofilter)
[![npm downloads](https://img.shields.io/npm/dm/1eurofilter.svg?style=flat-square)](https://npm-stat.com/charts.html?package=1eurofilter)

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


## Doc

### constructor

• **new OneEuroFilter**(`freq`, `mincutoff`, `beta`, `dcutoff`)

Constructs a 1 euro filter.

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `freq` | `number` | `undefined` | An estimate of the frequency in Hz of the signal (> 0), if timestamps are not available. |
| `mincutoff` | `number` | `1.0` | Min cutoff frequency in Hz (> 0). Lower values allow to remove more jitter. |
| `beta` | `number` | `0.0` | Parameter to reduce latency (> 0). |
| `dcutoff` | `number` | `1.0` | Used to filter the derivates. 1 Hz by default. Change this parameter if you know what you are doing. |


### filter

▸ **filter**(`value`, `timestamp`): `number`

Returns the filtered value.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `value` | `number` | Noisy value to filter |
| `timestamp` | `number` | (optional) timestamp in seconds |

### reset

▸ **reset**(): `void`

Resets the internal state of the filter.

### setBeta

▸ **setBeta**(`beta`): `void`

Sets the Beta parameter

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `beta` | `number` | Parameter to reduce latency (> 0). |

### setDerivateCutoff

▸ **setDerivateCutoff**(`dcutoff`): `void`

Sets the dcutoff parameter

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `dcutoff` | `number` | Used to filter the derivates. 1 Hz by default. Change this parameter if you know what you are doing. |

### setFrequency

▸ **setFrequency**(`freq`): `void`

Sets the frequency of the signal

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `freq` | `number` | An estimate of the frequency in Hz of the signal (> 0), if timestamps are not available. |

### setMinCutoff

▸ **setMinCutoff**(`mincutoff`): `void`

Sets the filter min cutoff frequency

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `mincutoff` | `number` | Min cutoff frequency in Hz (> 0). Lower values allow to remove more jitter. |

### setParameters

▸ **setParameters**(`freq`, `mincutoff`, `beta`): `void`

Sets the parameters of the 1 euro filter.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `freq` | `number` | An estimate of the frequency in Hz of the signal (> 0), if timestamps are not available. |
| `mincutoff` | `number` | Min cutoff frequency in Hz (> 0). Lower values allow to remove more jitter. |
| `beta` | `number` | Parameter to reduce latency (> 0). |


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

