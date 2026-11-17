using System;
using UnityEngine;

namespace OneEuroFilter
{
    /// <summary>
    /// One Euro Filter implementation for Unity Vector3 values.
    /// Each axis is filtered independently.
    /// </summary>
    public sealed class OneEuroFilter3
    {
        private const float TwoPi = 2f * Mathf.PI;

        private Vector3 previousRaw;

        public bool IsReady { get; private set; }
        public Vector3 Value { get; private set; }
        public Vector3 Derivative { get; private set; }

        /// <summary>
        /// Resets the filter state.
        /// </summary>
        public void Reset()
        {
            IsReady = false;
            Value = Vector3.zero;
            Derivative = Vector3.zero;
            previousRaw = Vector3.zero;
        }

        /// <summary>
        /// Filters a Vector3 sample.
        /// </summary>
        /// <param name="x">Raw input value.</param>
        /// <param name="dt">Time between samples in seconds.</param>
        /// <param name="minCutoff">Minimum cutoff frequency in Hz.</param>
        /// <param name="beta">Speed coefficient.</param>
        /// <param name="derivativeCutoff">Derivative cutoff frequency in Hz.</param>
        /// <returns>The filtered value.</returns>
        public Vector3 Step(Vector3 x, float dt, float minCutoff, float beta, float derivativeCutoff)
        {
            if (IsFinite(minCutoff) == false || minCutoff <= 0f)
            {
                throw new ArgumentOutOfRangeException(nameof(minCutoff));
            }

            if (IsFinite(beta) == false || beta < 0f)
            {
                throw new ArgumentOutOfRangeException(nameof(beta));
            }

            if (IsFinite(derivativeCutoff) == false || derivativeCutoff <= 0f)
            {
                throw new ArgumentOutOfRangeException(nameof(derivativeCutoff));
            }

            if (IsFinite(x) == false)
            {
                return Value;
            }

            if (IsReady == false)
            {
                IsReady = true;
                Value = x;
                previousRaw = x;
                Derivative = Vector3.zero;

                return Value;
            }

            if (IsFinite(dt) == false || dt <= 0f)
            {
                return Value;
            }

            Vector3 rawDerivative = (x - previousRaw) / dt;

            if (IsFinite(rawDerivative) == false)
            {
                return Value;
            }

            float derivativeAlpha = Alpha(derivativeCutoff, dt);
            Vector3 smoothedDerivative = Derivative + derivativeAlpha * (rawDerivative - Derivative);

            if (IsFinite(smoothedDerivative) == false)
            {
                return Value;
            }

            float cutoffX = minCutoff + beta * Mathf.Abs(smoothedDerivative.x);
            float cutoffY = minCutoff + beta * Mathf.Abs(smoothedDerivative.y);
            float cutoffZ = minCutoff + beta * Mathf.Abs(smoothedDerivative.z);

            float alphaX = Alpha(cutoffX, dt);
            float alphaY = Alpha(cutoffY, dt);
            float alphaZ = Alpha(cutoffZ, dt);

            Vector3 filtered = new Vector3(
                Value.x + alphaX * (x.x - Value.x),
                Value.y + alphaY * (x.y - Value.y),
                Value.z + alphaZ * (x.z - Value.z)
            );

            if (IsFinite(filtered) == false)
            {
                return Value;
            }

            previousRaw = x;
            Derivative = smoothedDerivative;
            Value = filtered;

            return Value;
        }

        private static float Alpha(float cutoff, float dt)
        {
            float scaled = TwoPi * cutoff * dt;

            if (float.IsPositiveInfinity(scaled))
            {
                return 1f;
            }

            return scaled / (1f + scaled);
        }

        private static bool IsFinite(Vector3 value)
        {
            return IsFinite(value.x) && IsFinite(value.y) && IsFinite(value.z);
        }

        private static bool IsFinite(float value)
        {
            return float.IsNaN(value) == false && float.IsInfinity(value) == false;
        }
    }
}