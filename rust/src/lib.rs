//! # 1€ filter (Rust)
//!
//! A faithful port of the reference C++ implementation in `../cpp`
//! (Casiez, Roussel & Vogel, *1€ Filter: A Simple Speed-Based Low-Pass Filter
//! for Noisy Input in Interactive Systems*, CHI '12). It matches the reference
//! numerically, including the 08/2023 fix that estimates the derivative from
//! the last *filtered* value rather than the last raw value.
//!
//! A first-order low-pass whose cutoff adapts to speed: low cutoff (heavy
//! smoothing) when the signal is slow, higher cutoff (less lag) when it moves
//! fast. Two intuitive parameters: `mincutoff` sets the jitter floor at rest,
//! `beta` sets how aggressively lag is traded away as speed rises.

use std::f64::consts::PI;

/// Clamp `alpha` into `(0, 1]`. The reference throws on out-of-range values;
/// its exception-free build falls back to `0.5`, which we mirror.
fn clamp_alpha(alpha: f64) -> f64 {
    if alpha <= 0.0 || alpha > 1.0 {
        0.5
    } else {
        alpha
    }
}

/// Exponential low-pass filter: `s <- a*value + (1-a)*s`, seeded on first use.
pub struct LowPassFilter {
    y: f64,
    s: f64,
    a: f64,
    initialized: bool,
}

impl LowPassFilter {
    pub fn new(alpha: f64) -> Self {
        Self {
            y: 0.0,
            s: 0.0,
            a: clamp_alpha(alpha),
            initialized: false,
        }
    }

    fn set_alpha(&mut self, alpha: f64) {
        self.a = clamp_alpha(alpha);
    }

    pub fn filter(&mut self, value: f64) -> f64 {
        let result = if self.initialized {
            self.a * value + (1.0 - self.a) * self.s
        } else {
            self.initialized = true;
            value
        };
        self.y = value;
        self.s = result;
        result
    }

    pub fn filter_with_alpha(&mut self, value: f64, alpha: f64) -> f64 {
        self.set_alpha(alpha);
        self.filter(value)
    }

    pub fn has_last_raw_value(&self) -> bool {
        self.initialized
    }

    pub fn last_filtered_value(&self) -> f64 {
        self.s
    }
}

/// The 1€ filter.
pub struct OneEuroFilter {
    freq: f64,
    mincutoff: f64,
    beta: f64,
    dcutoff: f64,
    x: LowPassFilter,
    dx: LowPassFilter,
    lasttime: Option<f64>,
}

impl OneEuroFilter {
    /// * `freq` — estimated sampling frequency in Hz (used until timestamps
    ///   give a better estimate).
    /// * `mincutoff` — min cutoff frequency in Hz; lower removes more jitter.
    /// * `beta` — latency-reduction gain; higher tracks faster motion tighter.
    /// * `dcutoff` — cutoff for the derivative low-pass (1 Hz by default).
    pub fn new(freq: f64, mincutoff: f64, beta: f64, dcutoff: f64) -> Self {
        let freq = if freq > 0.0 { freq } else { 120.0 };
        let mincutoff = if mincutoff > 0.0 { mincutoff } else { 1.0 };
        let dcutoff = if dcutoff > 0.0 { dcutoff } else { 1.0 };
        let mut filter = Self {
            freq,
            mincutoff,
            beta,
            dcutoff,
            x: LowPassFilter::new(1.0),
            dx: LowPassFilter::new(1.0),
            lasttime: None,
        };
        let a_min = filter.alpha(mincutoff);
        let a_d = filter.alpha(dcutoff);
        filter.x = LowPassFilter::new(a_min);
        filter.dx = LowPassFilter::new(a_d);
        filter
    }

    fn alpha(&self, cutoff: f64) -> f64 {
        let te = 1.0 / self.freq;
        let tau = 1.0 / (2.0 * PI * cutoff);
        1.0 / (1.0 + tau / te)
    }

    /// Filter `value` sampled at `timestamp` (seconds). Returns the smoothed
    /// value.
    pub fn filter(&mut self, value: f64, timestamp: f64) -> f64 {
        if let Some(last) = self.lasttime {
            if timestamp > last {
                self.freq = 1.0 / (timestamp - last);
            }
        }
        self.lasttime = Some(timestamp);

        // Estimate the variation per second from the last *filtered* value.
        let dvalue = if self.x.has_last_raw_value() {
            (value - self.x.last_filtered_value()) * self.freq
        } else {
            0.0
        };
        let a_d = self.alpha(self.dcutoff);
        let edvalue = self.dx.filter_with_alpha(dvalue, a_d);

        // Speed-adaptive cutoff, then filter the value with it.
        let cutoff = self.mincutoff + self.beta * edvalue.abs();
        let a_c = self.alpha(cutoff);
        self.x.filter_with_alpha(value, a_c)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn low_pass_seeds_then_blends() {
        let mut lp = LowPassFilter::new(0.5);
        assert_eq!(lp.filter(10.0), 10.0, "first sample passes through");
        assert_eq!(lp.filter(0.0), 5.0, "0.5*0 + 0.5*10");
    }

    /// A constant input converges to that constant (zero steady-state error).
    #[test]
    fn converges_to_constant() {
        let mut f = OneEuroFilter::new(120.0, 1.0, 0.1, 1.0);
        let mut out = 0.0;
        for i in 0..2000 {
            out = f.filter(5.0, i as f64 / 120.0);
        }
        assert!((out - 5.0).abs() < 1e-6, "out={out}");
    }

    /// alpha is the reference's `1/(1 + tau/te)`, always in (0, 1].
    #[test]
    fn alpha_matches_reference_formula() {
        let f = OneEuroFilter::new(120.0, 1.0, 0.1, 1.0);
        let te = 1.0 / 120.0;
        let tau = 1.0 / (2.0 * PI * 1.0);
        let expected = 1.0 / (1.0 + tau / te);
        assert!((f.alpha(1.0) - expected).abs() < 1e-15);
        assert!(f.alpha(1.0) > 0.0 && f.alpha(1.0) <= 1.0);
    }
}
