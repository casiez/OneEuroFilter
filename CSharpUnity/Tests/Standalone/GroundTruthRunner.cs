using System;
using System.Globalization;
using System.IO;
using UnityEngine;

namespace OneEuroFilter
{
    public static class GroundTruthRunner
    {
        public static int Main(string[] args)
        {
            if (args.Length != 1)
            {
                Console.Error.WriteLine("Usage: GroundTruthRunner groundTruth.csv");
                return 1;
            }

            CultureInfo culture = CultureInfo.InvariantCulture;
            OneEuroFilter3 filter = new OneEuroFilter3();

            const float minCutoff = 1f;
            const float beta = 0.1f;
            const float derivativeCutoff = 1f;

            float previousTimestamp = 0f;
            bool firstSample = true;

            Console.WriteLine("timestamp,noisy,filtered");

            using (StreamReader reader = new StreamReader(args[0]))
            {
                reader.ReadLine();

                string line;
                while ((line = reader.ReadLine()) != null)
                {
                    if (string.IsNullOrWhiteSpace(line))
                    {
                        continue;
                    }

                    string[] columns = line.Split(',');
                    if (columns.Length != 4)
                    {
                        throw new FormatException("Invalid CSV row: " + line);
                    }

                    float timestamp = float.Parse(columns[0], culture);
                    float noisy = float.Parse(columns[2], culture);

                    float dt = firstSample
                        ? 1f / 120f
                        : timestamp - previousTimestamp;

                    if (dt <= 0f)
                    {
                        throw new FormatException("Timestamps must be increasing.");
                    }

                    Vector3 input = new Vector3(noisy, 0f, 0f);
                    Vector3 result = filter.Step(input, dt, minCutoff, beta, derivativeCutoff);

                    Console.WriteLine(columns[0] + "," + columns[2] + "," + result.x.ToString("R", culture));

                    previousTimestamp = timestamp;
                    firstSample = false;
                }
            }

            return 0;
        }
    }
}
