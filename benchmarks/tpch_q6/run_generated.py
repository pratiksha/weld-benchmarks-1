import sys
import subprocess
from argparse import ArgumentParser as ap

cols = 50
nitems=10000000
sels=["0.5"]
passes = {"predicated" : "\"loop-fusion unroll-static-loop infer-size inline-literals unroll-structs inline-let inline-let-getfield predicate vectorize\"",
          "branched"   : "\"loop-fusion unroll-static-loop infer-size inline-literals unroll-structs short-circuit-booleans inline-let inline-let-getfield vectorize\"",
          "dynamic"    : "\"loop-fusion unroll-static-loop infer-size inline-literals unroll-structs inline-let inline-let-getfield measurement inline-let inline-let-getfield vectorize short-circuit-booleans\""}

def run_microbench(n, outfile):
    for name, pass_list in passes.iteritems():
        for sel in sels:
            s_results = []
            for i in range(33, 45):
                results = []
                for j in range(n):
                    subprocess.check_output("python generate_benchmarks.py %d %d > generated.weld" % (i, cols), shell=True)
                    output = subprocess.check_output("./gen -n %d -c %d -m %d -s %s -p %s" % (nitems, cols, i, sel, pass_list), shell=True)
                    output = output.decode('utf-8')
                    time, result = output.split("\t")
                    print result
                    results.append(time)
                s_results.append(','.join([str(x) for x in results]))
            fname = "%s_%s_%s.csv" % (outfile, name, sel)
            with open(fname, 'w') as f:
                for row in s_results:
                    f.write(row + '\n')

def main():
    parser = ap()
    parser.add_argument('-n', "--num_iterations", type=int, required=True,
                        help="Number of iterations to run each benchmark")
    parser.add_argument('-f', "--file_prefix", type=str, required=True,
                        help="Prefix for files to dump output in")

    args = parser.parse_args()
    run_microbench(args.num_iterations, args.file_prefix)
    
if __name__ == '__main__':
    main()
