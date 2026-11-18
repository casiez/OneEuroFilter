#if !UNITY_5_3_OR_NEWER

using System;

namespace UnityEngine
{
    public struct Vector3
    {
        public float x;
        public float y;
        public float z;

        public Vector3(float x, float y, float z)
        {
            this.x = x;
            this.y = y;
            this.z = z;
        }

        public static Vector3 zero
        {
            get
            {
                return new Vector3(0f, 0f, 0f);
            }
        }

        public static Vector3 operator +(Vector3 a, Vector3 b)
        {
            return new Vector3(a.x + b.x, a.y + b.y, a.z + b.z);
        }

        public static Vector3 operator -(Vector3 a, Vector3 b)
        {
            return new Vector3(a.x - b.x, a.y - b.y, a.z - b.z);
        }

        public static Vector3 operator *(float scalar, Vector3 v)
        {
            return new Vector3(
                scalar * v.x,
                scalar * v.y,
                scalar * v.z
            );
        }

        public static Vector3 operator /(Vector3 v, float scalar)
        {
            return new Vector3(
                v.x / scalar,
                v.y / scalar,
                v.z / scalar
            );
        }
    }

    public static class Mathf
    {
        public const float PI = (float)Math.PI;

        public static float Abs(float value)
        {
            return Math.Abs(value);
        }
    }
}
#endif