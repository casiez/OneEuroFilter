using System;
using NUnit.Framework;
using UnityEngine;

namespace OneEuroFilter
{
    public sealed class OneEuroFilter3Tests
    {
        private OneEuroFilter3 _filter;

        [SetUp]
        public void SetUp()
        {
            _filter = new OneEuroFilter3();
        }

        [Test]
        public void FirstSampleInitializesFilter()
        {
            Vector3 input = new Vector3(1f, 2f, 3f);

            Assert.AreEqual(input, _filter.Step(input, 0.016f, 1f, 0f, 1f));
            Assert.IsTrue(_filter.IsReady);
            Assert.AreEqual(Vector3.zero, _filter.Derivative);
        }

        [Test]
        public void ResetClearsState()
        {
            _filter.Step(Vector3.one, 0.016f, 1f, 0f, 1f);
            _filter.Reset();

            Assert.IsFalse(_filter.IsReady);
            Assert.AreEqual(Vector3.zero, _filter.Value);
            Assert.AreEqual(Vector3.zero, _filter.Derivative);
        }

        [Test]
        public void InvalidInputDoesNotUpdateState()
        {
            _filter.Step(Vector3.one, 0.016f, 1f, 0f, 1f);

            Vector3 invalid = new Vector3(float.NaN, 2f, 3f);

            Assert.AreEqual(Vector3.one, _filter.Step(invalid, 0.016f, 1f, 0f, 1f));
            Assert.AreEqual(Vector3.one, _filter.Value);
        }

        [Test]
        public void AxesAreFilteredIndependently()
        {
            _filter.Step(Vector3.zero, 0.016f, 1f, 0.5f, 1f);

            Vector3 result = _filter.Step(new Vector3(10f, 0f, 0f), 0.016f, 1f, 0.5f, 1f);

            Assert.Greater(result.x, 0f);
            Assert.AreEqual(0f, result.y);
            Assert.AreEqual(0f, result.z);
        }

        [Test]
        public void InvalidParametersThrow()
        {
            Assert.Throws<ArgumentOutOfRangeException>(() =>
            {
                _filter.Step(Vector3.zero, 0.016f, -1f, 0f, 1f);
            });

            Assert.Throws<ArgumentOutOfRangeException>(() =>
            {
                _filter.Step(Vector3.zero, 0.016f, 1f, -1f, 1f);
            });

            Assert.Throws<ArgumentOutOfRangeException>(() =>
            {
                _filter.Step(Vector3.zero, 0.016f, 1f, 0f, 0f);
            });
        }
    }
}