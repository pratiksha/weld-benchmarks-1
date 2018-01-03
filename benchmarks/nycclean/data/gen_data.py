import pandas as pd
import numpy as np
import sys

if len(sys.argv) != 3:
        print "Usage: {} <filename> <branch pass probability>".format(sys.argv[0])
        sys.exit(1)

filename = sys.argv[1]
prob = float(sys.argv[2])

print "Branch will pass with probability", prob

df = pd.read_csv(filename)
# With probability `prob`, the predicate will pass (i.e., have a non-zero value).
df[" trip_distance"] = 0.0 #np.random.choice([0, 1], size=len(df[" trip_distance"]), p=[1 - prob, prob])
df.to_csv(filename + "." + str(prob))

print "Wrote output to {}".format(filename + "." + str(prob))
