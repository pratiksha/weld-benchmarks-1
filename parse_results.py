def parse(filename):
    with open(filename) as f:
        lines = [line for line in f]

    # Print All, -Loop Fusion, -Infer Size, -Predicate, and -Vectorize.

    lines = lines[1:]
    lines = [l.split('\t') for l in lines]
    lines = [[l.strip() for l in line] for line in lines]

    print lines[0]

    # Get the all 
    all_transforms_lines = [line for line in lines if line[2].find("p=\"\"\"\"") != -1]
    no_loop_fusion = [line for line in lines if line[2].find("loop-fusion") == -1]
    no_infer_size = [line for line in lines if line[2].find("infer-size") == -1]
    no_predicate = [line for line in lines if line[2].find("predicate") == -1]
    no_vectorize = [line for line in lines if line[2].find("vectorize") == -1]

    print "All"
    format_lines(all_transforms_lines)
    print ""

    print "-Loop Fusion"
    format_lines(no_loop_fusion)
    print ""

    print "-Infer Size"
    format_lines(no_infer_size)
    print ""

    print "-Predicate"
    format_lines(no_predicate)
    print ""

    print "-Vectorize"
    format_lines(no_vectorize)
    print ""

def format_lines(lines, trials=1):
    for line in lines:
        if line[1] == "Python->Weld":
            pytoweld = line[3]
            for i in xrange(1, trials-1):
                pytoweld += line[3+i]
        if line[1] == "Weld":
            weld = line[3]
            for i in xrange(1, trials-1):
                weld += line[3+i]
        if line[1] == "Weld compile time":
            weldcompile = line[3]
            for i in xrange(1, trials-1):
                weldcompile += line[3+i]
        if line[1] == "Weld->Python":
            weldtopy = line[3]
            for i in xrange(1, trials-1):
                weldtopy += line[3+i]
        if line[1] == "End-to-End":
            e2e = line[3]
            for i in xrange(1, trials-1):
                e2e += line[3+i]

    final = "{}\n{}\n{}\n{}\n{}".format(pytoweld, weld, weldcompile, weldtopy, e2e)
    print final

if __name__=="__main__":
    parse("nyc.results.2")

