# -*- coding: utf-8 -*-
#
# OneEuroFilter.py -
#
# Authors: 
# Nicolas Roussel (nicolas.roussel@inria.fr)
# Géry Casiez https://gery.casiez.net
#
# Copyright 2019 Inria
# 
# BSD License https://opensource.org/licenses/BSD-3-Clause
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions
# and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
# and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or
# promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import math

# ----------------------------------------------------------------------------

class LowPassFilter(object):

    def __init__(self, alpha:float) -> None:
        self.__setAlpha(alpha)
        self.__y = self.__s = None

    def __setAlpha(self, alpha:float) -> None:
        alpha = float(alpha)
        if alpha<=0 or alpha>1.0:
            raise ValueError("alpha (%s) should be in (0.0, 1.0]"%alpha)
        self.__alpha = alpha

    def __call__(self, value:float, timestamp:float=None, alpha:float=None) -> float:        
        if alpha is not None:
            self.__setAlpha(alpha)
        if self.__y is None:
            s = value
        else:
            s = self.__alpha*value + (1.0-self.__alpha)*self.__s
        self.__y = value
        self.__s = s
        return s

    def lastValue(self) -> float:
        return self.__y
    
    def lastFilteredValue(self) -> float:
        return self.__s
    
    def reset(self) -> None:
        self.__y = None

# ----------------------------------------------------------------------------

class OneEuroFilter(object):

    def __init__(self, freq:float, mincutoff:float=1.0, beta:float=0.0, dcutoff:float=1.0) -> None:
        """ Initializes the One Euro Filter
        
        :param freq: An estimate of the frequency in Hz of the signal (> 0), if timestamps are not available.
        :type freq: float
        :param mincutoff: Min cutoff frequency in Hz (> 0). Lower values allow to remove more jitter.
        :type mincutoff: float, optional
        :param  beta: Parameter to reduce latency (> 0).
        :type beta: float, optional
        :param  dcutoff: Used to filter the derivates. 1 Hz by default. Change this parameter if you know what you are doing.
        :type dcutoff: float, optional
        :raises ValueError: If one of the parameters is not >0
        """

        if freq<=0:
            raise ValueError("freq should be >0")
        if mincutoff<=0:
            raise ValueError("mincutoff should be >0")
        if dcutoff<=0:
            raise ValueError("dcutoff should be >0")
        self.__freq = float(freq)
        self.__mincutoff = float(mincutoff)
        self.__beta = float(beta)
        self.__dcutoff = float(dcutoff)
        self.__x = LowPassFilter(self.__alpha(self.__mincutoff))
        self.__dx = LowPassFilter(self.__alpha(self.__dcutoff))
        self.__lasttime = None
        
    def __alpha(self, cutoff:float) -> float:
        """Computes the alpha value from a cutoff frequency.

        :param cutoff: cutoff frequency in Hz (> 0).
        :type cutoff: float
        :returns:  the alpha value to be used for the low pass filter
        :rtype: float
        """

        te    = 1.0 / self.__freq
        tau   = 1.0 / (2*math.pi*cutoff)
        return  1.0 / (1.0 + tau/te)

    def __call__(self, x:float, timestamp:float=None) -> float:
        """Filters a noisy value.

        :param x: Noisy value to filter.
        :type x: float
        :param timestamp: timestamp in seconds.
        :type timestamp: float, optional
        :returns: the filtered value
        :rtype: float
        """

        # ---- update the sampling frequency based on timestamps
        if self.__lasttime and timestamp and timestamp>self.__lasttime:
            self.__freq = 1.0 / (timestamp-self.__lasttime)
        self.__lasttime = timestamp
        # ---- estimate the current variation per second
        prev_x = self.__x.lastFilteredValue()
        dx = 0.0 if prev_x is None else (x-prev_x)*self.__freq # FIXME: 0.0 or value?
        edx = self.__dx(dx, timestamp, alpha=self.__alpha(self.__dcutoff))
        # ---- use it to update the cutoff frequency
        cutoff = self.__mincutoff + self.__beta*math.fabs(edx)
        # ---- filter the given value
        return self.__x(x, timestamp, alpha=self.__alpha(cutoff))

    def filter(self, x:float, timestamp:float=None) -> float:
        """Filters a noisy value.

        :param x: Noisy value to filter.
        :type x: float
        :param timestamp: timestamp in seconds.
        :type timestamp: float, optional
        :returns: the filtered value
        :rtype: float
        """

        return self.__call__(x, timestamp)

    def setFrequency(self, freq: float) -> None:
        """Sets the frequency of the input signal.

        :param freq: An estimate of the frequency in Hz of the signal (> 0), if timestamps are not available.
        :type freq: float
        :raises ValueError: If one of the frequency is not >0
        """

        if freq<=0:
            raise ValueError("freq should be >0")
        else:
            self.__freq = float(freq) 
    
    def setMinCutoff(self, mincutoff:float) -> None:
        """Sets the filter min cutoff frequency.

        :param mincutoff: Min cutoff frequency in Hz (> 0). Lower values allow to remove more jitter.
        :type mincutoff: float
        :raises ValueError: If one of the frequency is not >0            
        """

        if mincutoff<=0:
            raise ValueError("mincutoff should be >0")
        else:
            self.__mincutoff = float(mincutoff)
    
    def setBeta(self, beta:float) -> None:
        """Sets the Beta parameter.

        :param beta: Parameter to reduce latency (> 0).
        :type beta: float            
        """

        self.__beta = float(beta)

    def setDerivateCutoff(self, dcutoff:float) -> None:
        """Sets the dcutoff parameter.

        :param dcutoff: Used to filter the derivates. 1 Hz by default. Change this parameter if you know what you are doing.
        :type dcutoff: float              
        """

        self.__dcutoff = float(dcutoff)
    
    def setParameters(self, freq: float,  mincutoff: float=1.0, beta:float=0.0, dcutoff=1.0) -> None:
        """Sets all the parameters of the filter.
  
        :param freq: An estimate of the frequency in Hz of the signal (> 0), if timestamps are not available.
        :type freq: float
        :param mincutoff: Min cutoff frequency in Hz (> 0). Lower values allow to remove more jitter.
        :type mincutoff: float, optional
        :param  beta: Parameter to reduce latency (> 0).
        :type beta: float, optional
        :param  dcutoff: Used to filter the derivates. 1 Hz by default. Change this parameter if you know what you are doing.
        :type dcutoff: float, optional
        :raises ValueError: If one of the parameters is not >0
        """

        self.setFrequency(freq)
        self.setMinCutoff(mincutoff)
        self.setBeta(beta)
        self.setDerivateCutoff(dcutoff)

    def reset(self) -> None:
        """Resets the internal state of the filter."""

        self.__x.reset()
        self.__dx.reset()
        self.__lasttime = None

# ----------------------------------------------------------------------------
