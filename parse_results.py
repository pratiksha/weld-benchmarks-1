def parse(filename):
    with open(filename) as f:
        lines = [line for line in f]

    # Print All, -Loop Fusion, -Infer Size, -Predicate, and -Vectorize.

    lines = lines[1:]
    lines = [l.split('\t') for l in lines]
    lines = [[l.strip() for l in line] for line in lines]

    # Get the all 
    all_transforms_lines = [line for line in lines if line[2].find("p=\"\"\"\"") != -1]
    no_loop_fusion = [line for line in lines if line[2].find("loop-fusion") == -1]
    no_infer_size = [line for line in lines if line[2].find("infer-size") == -1]
    no_predicate = [line for line in lines if line[2].find("predicate") == -1]
    no_vectorize = [line for line in lines if line[2].find("vectorize") == -1]

    format_lines(all_transforms_lines)
    print ""

    print ""
    format_lines(no_loop_fusion)
    print ""

    print ""
    format_lines(no_infer_size)
    print ""

    print ""
    format_lines(no_predicate)
    print ""

    print ""
    format_lines(no_vectorize)

def format_lines(lines, trials=5):
    for line in lines:
        if line[1] == "Python->Weld":
            pytoweld = line[3]
            for i in xrange(1, trials):
                pytoweld += "\t" + line[3+i]
        if line[1] == "Weld":
            weld = line[3]
            for i in xrange(1, trials):
                weld += "\t" + line[3+i]
        if line[1] == "Weld compile time":
            weldcompile = line[3]
            for i in xrange(1, trials):
                weldcompile += "\t" + line[3+i]
        if line[1] == "Weld->Python":
            weldtopy = line[3]
            for i in xrange(1, trials):
                weldtopy += "\t" + line[3+i]
        if line[1] == "End-to-End":
            e2e = line[3]
            for i in xrange(1, trials):
                e2e += "\t" + line[3+i]

    final = "{}\n{}\n{}\n{}\n{}".format(pytoweld, weld, weldcompile, weldtopy, e2e)
    print final

if __name__=="__main__":
    parse("nyc.results")

