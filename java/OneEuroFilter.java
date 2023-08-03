/**
 *
 * @author s. conversy from n. roussel c++ version
 *
 * Copyright 2019 
 * 
 * BSD License https://opensource.org/licenses/BSD-3-Clause
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *  1. Redistributions of source code must retain the above copyright notice, this list of conditions
 * and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
 * and the following disclaimer in the documentation and/or other materials provided with the distribution.
 * 
 * 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or
 * promote products derived from this software without specific prior written permission.

 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
 * INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 */
class LowPassFilter {

    double y, a, s;
    boolean initialized;

    void setAlpha(double alpha) throws Exception {
        if (alpha <= 0.0 || alpha > 1.0) {
            throw new Exception("alpha should be in (0.0., 1.0]");
        }
        a = alpha;
    }

    public LowPassFilter(double alpha) throws Exception {
        init(alpha, 0);
    }

    public LowPassFilter(double alpha, double initval) throws Exception {
        init(alpha, initval);
    }

    private void init(double alpha, double initval) throws Exception {
        y = s = initval;
        setAlpha(alpha);
        initialized = false;
    }

    public double filter(double value) {
        double result;
        if (initialized) {
            result = a * value + (1.0 - a) * s;
        } else {
            result = value;
            initialized = true;
        }
        y = value;
        s = result;
        return result;
    }

    public double filterWithAlpha(double value, double alpha) throws Exception {
        setAlpha(alpha);
        return filter(value);
    }

    public boolean hasLastRawValue() {
        return initialized;
    }

    public double lastRawValue() {
        return y;
    }

    public double lastFilteredValue() {
        return s;
    }
};

public class OneEuroFilter {

    double freq;
    double mincutoff;
    double beta_;
    double dcutoff;
    LowPassFilter x;
    LowPassFilter dx;
    double lasttime;
    static double UndefinedTime = -1;

    double alpha(double cutoff) {
        double te = 1.0 / freq;
        double tau = 1.0 / (2 * Math.PI * cutoff);
        return 1.0 / (1.0 + tau / te);
    }

    void setFrequency(double f) throws Exception {
        if (f <= 0) {
            throw new Exception("freq should be >0");
        }
        freq = f;
    }

    void setMinCutoff(double mc) throws Exception {
        if (mc <= 0) {
            throw new Exception("mincutoff should be >0");
        }
        mincutoff = mc;
    }

    void setBeta(double b) {
        beta_ = b;
    }

    void setDerivateCutoff(double dc) throws Exception {
        if (dc <= 0) {
            throw new Exception("dcutoff should be >0");
        }
        dcutoff = dc;
    }

    public OneEuroFilter(double freq) throws Exception {
        init(freq, 1.0, 0.0, 1.0);
    }

    public OneEuroFilter(double freq, double mincutoff) throws Exception {
        init(freq, mincutoff, 0.0, 1.0);
    }

    public OneEuroFilter(double freq, double mincutoff, double beta_) throws Exception {
        init(freq, mincutoff, beta_, 1.0);
    }

    public OneEuroFilter(double freq, double mincutoff, double beta_, double dcutoff) throws Exception {
        init(freq, mincutoff, beta_, dcutoff);
    }

    private void init(double freq,
            double mincutoff, double beta_, double dcutoff) throws Exception {
        setFrequency(freq);
        setMinCutoff(mincutoff);
        setBeta(beta_);
        setDerivateCutoff(dcutoff);
        x = new LowPassFilter(alpha(mincutoff));
        dx = new LowPassFilter(alpha(dcutoff));
        lasttime = UndefinedTime;
    }

    double filter(double value) throws Exception {
        return filter(value, UndefinedTime);
    }

    double filter(double value, double timestamp) throws Exception {
        // update the sampling frequency based on timestamps
        if (lasttime != UndefinedTime && timestamp != UndefinedTime) {
            freq = 1.0 / (timestamp - lasttime);
        }
        
        lasttime = timestamp;
        // estimate the current variation per second
        double dvalue = x.hasLastRawValue() ? (value - x.lastFilteredValue()) * freq : 0.0; // FIXME: 0.0 or value?
        double edvalue = dx.filterWithAlpha(dvalue, alpha(dcutoff));
        // use it to update the cutoff frequency
        double cutoff = mincutoff + beta_ * Math.abs(edvalue);
        // filter the given value
        return x.filterWithAlpha(value, alpha(cutoff));
    }

}
