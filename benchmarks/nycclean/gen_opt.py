import itertools

opts = "loop-fusion unroll-static-loop inline-literals unroll-structs short-circuit-booleans inline-let predicate vectorize".split(' ')

combs = []
for i in range(len(opts)):
    combs.extend([list(x) for x in itertools.combinations(opts, i)])

for c in combs:
    print "\"" + ' '.join(c) + "\","
