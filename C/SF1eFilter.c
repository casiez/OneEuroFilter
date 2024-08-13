/**
 One Euro Filter, C version
 
 Copyright (c) 2014 Jonathan Aceituno <join@oin.name>

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.

 07/12/20: added MIT license
 03/08/23: fixed version (Géry Casiez)
 
 For details, see https://gery.casiez.net/1euro/
 */

#include "SF1eFilter.h"
#include <stdlib.h>
#include <math.h>

SFLowPassFilter *SFLowPassFilterCreate()
{
	SFLowPassFilter *filter = (SFLowPassFilter *)malloc(sizeof(SFLowPassFilter));
	SFLowPassFilterInit(filter);
	return filter;
}

SFLowPassFilter *SFLowPassFilterDestroy(SFLowPassFilter *filter)
{
	free(filter);
	return ((void*)0);
}

void SFLowPassFilterInit(SFLowPassFilter *filter)
{
	filter->usedBefore = 0;
	filter->hatxprev = 0;
	filter->xprev = 0;
}

float SFLowPassFilterDo(SFLowPassFilter *filter, float x, float alpha) {
	if(!filter->usedBefore) {
		filter->usedBefore = 1;
		filter->hatxprev = x;
	}
	float hatx = alpha * x + (1.f - alpha) * filter->hatxprev;
	filter->xprev = x;
	filter->hatxprev = hatx;
	return hatx;
}

SF1eFilter *SF1eFilterCreate(float frequency, float minCutoffFrequency, float cutoffSlope, float derivativeCutoffFrequency)
{
	SF1eFilterConfiguration config;
	config.frequency = frequency;
	config.minCutoffFrequency = minCutoffFrequency;
	config.cutoffSlope = cutoffSlope;
	config.derivativeCutoffFrequency = derivativeCutoffFrequency;
	return SF1eFilterCreateWithConfig(config);
}

SF1eFilter *SF1eFilterCreateWithConfig(SF1eFilterConfiguration config)
{
	SF1eFilter *filter = (SF1eFilter *)malloc(sizeof(SF1eFilter));
	filter->config = config;
	return filter;
}

SF1eFilter *SF1eFilterDestroy(SF1eFilter *filter)
{
	free(filter);
	return ((void*)0);
}

void SF1eFilterInit(SF1eFilter *filter)
{
	filter->frequency = filter->config.frequency;
	filter->lastTime = 0;
	SFLowPassFilterInit(&(filter->xfilt));
	SFLowPassFilterInit(&(filter->dxfilt));
}

float SF1eFilterDo(SF1eFilter *filter, float x)
{
	float dx = 0.f;
	
	if(filter->lastTime == 0 && filter->frequency != filter->config.frequency) {
		filter->frequency = filter->config.frequency;
	}
	
	if(filter->xfilt.usedBefore) {
		dx = (x - filter->xfilt.hatxprev) * filter->frequency;
	}
	
	float edx = SFLowPassFilterDo(&(filter->dxfilt), dx, SF1eFilterAlpha(filter, filter->config.derivativeCutoffFrequency));
	float cutoff = filter->config.minCutoffFrequency + filter->config.cutoffSlope * fabsf(edx);
	return SFLowPassFilterDo(&(filter->xfilt), x, SF1eFilterAlpha(filter, cutoff));
}

float SF1eFilterDoAtTime(SF1eFilter *filter, float x, double timestamp)
{
	if(filter->lastTime != 0 && timestamp > filter->lastTime) {
		filter->frequency = 1.0f / (timestamp - filter->lastTime);
	}
	filter->lastTime = timestamp;
	float fx = SF1eFilterDo(filter, x);
	return fx;
}

float SF1eFilterAlpha(SF1eFilter *filter, float cutoff)
{
	float tau = 1.0f / (2.f * M_PI * cutoff);
	float te = 1.0f / filter->frequency;
	return 1.0f / (1.0f + tau / te);
}

