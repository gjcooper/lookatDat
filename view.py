from prespy.logfile import load
import matplotlib.pyplot as plt
import sys
from itertools import zip_longest
import json


def plot_codes(pfile, plot=True):
    codes = [e.code for e in pfile.events if e.etype == 'Sound']
    if not plot:
        return codes
    plt.plot(codes)
    plt.show()
    return codes

def plot_diffs(pfile, plot=True):
    times = [e.time for e in pfile.events if e.etype == 'Sound']
    diffs = [t - times[i] for i, t in enumerate(times[1:])]
    if not plot:
        return diffs
    plt.plot(diffs)
    plt.show()
    return diffs

def extract_ev2(efile):
    pcodes = [e[1] for e in efile if e[1] not in {'254', '251', '255'}]
    return pcodes

def compare_codes(codes, pcodes):
    mismatches = 0
    for i, c1, c2 in zip_longest(range(max(len(codes), len(pcodes))), codes, pcodes):
        if c1 != c2:
            print(i,c1,c2)
            mismatches += 1
        if mismatches > 20:
            print(len(codes), len(pcodes))
            break

def main_alt():
    fn = sys.argv[1]
    pfile = load(fn)
    with open(sys.argv[2], 'r') as efcnts:
        lines = efcnts.read().splitlines()
    efile = [l.split() for l in lines]
    codes = plot_codes(pfile, False)
    plot_diffs(pfile, False)
    pcodes = extract_ev2(efile)
    compare_codes(codes, pcodes)

def main(lf, ef):
    pfile = load(lf)
    with open(ef, 'r') as efcnts:
        lines = efcnts.read().splitlines()
    efile = [l.split() for l in lines]
    codes = plot_codes(pfile)
    plot_diffs(pfile)
    pcodes = extract_ev2(efile)
    compare_codes(codes, pcodes)

def runfromfile(jsfile):
    with open(jsfile, 'r') as jsonfile:
        dirdict = json.load(jsonfile)

    for key in dirdict:
        print(key)
        for filepair in dirdict[key]:
            main(*filepair)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
