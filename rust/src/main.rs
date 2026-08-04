//! Runs the 1€ filter over the same fixed noisy signal as the reference C++
//! test and prints `timestamp,noisy,filtered` for comparison against
//! `../groundTruth.csv` (see `../test.py`).

use one_euro_filter::OneEuroFilter;

mod data;

fn main() {
    let frequency = 120.0; // Hz
    let mincutoff = 1.0; // Hz
    let beta = 0.1;
    let dcutoff = 1.0;

    println!("timestamp,noisy,filtered");

    let mut f = OneEuroFilter::new(frequency, mincutoff, beta, dcutoff);
    for (&ts, &noisy) in data::TS.iter().zip(data::NOISY.iter()) {
        let filtered = f.filter(noisy, ts);
        println!("{ts},{noisy},{filtered}");
    }
}
