import sys

from csv import DictReader as dr
from csv import DictWriter as dw

def main():
    if len(sys.argv) != 4:
        print 'Usage: python extract_cols.py in_fname out_fname comma,separated,cols'
        return
    
    fname = sys.argv[1]
    cols = sys.argv[3].split(',')

    ret_rows = []
    with open(fname, 'r') as f:
        reader = dr(f)
        for row in reader:
            ret_r = []
            ret_r.append(row[''])
            for c in cols:
                ret_r.append(row[c])
            ret_rows.append(ret_r)
                
    with open(sys.argv[2], 'w') as of:
        of.write(',' + ','.join(cols) + '\n')
        for r in ret_rows:
            of.write(','.join([str(x) for x in r]) + '\n')
            
if __name__=='__main__':
    main()
