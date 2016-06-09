from prespy.logfile import load
from eegevt.eventfile import load_efile
import matplotlib.pyplot as plt
import sys
from itertools import zip_longest
import json


def compare_codes(codes, pcodes):
    mismatches = 0
    for i, c1, c2 in zip_longest(range(max(len(codes), len(pcodes))),
                                 codes, pcodes):
        if c1 != c2:
            print(i, c1, c2)
            mismatches += 1
        if mismatches > 20:
            print(len(codes), len(pcodes))
            break


def load_pair(lf, ef):
    pfile = load(lf)
    efile = load_efile(ef)
    # load codes
    pcodes = [e.code for e in pfile.events]
    ecodes = [d[efile.evtcode] for d in efile.data]
    # load time differences between events
    ptimes = [e.time for e in pfile.events]
    etimes = [d[efile.evttime] for d in efile.data]
    pdiffs = [t - ptimes[i] for i, t in enumerate(ptimes[1:])]
    ediffs = [(t - etimes[i])*1000 for i, t in enumerate(etimes[1:])]
    # Return report
    return dict(codes=(pcodes, ecodes), diffs=(pdiffs, ediffs))


def display(report):
    plt.figure(1)
    plt.hold = True
    ax = plt.subplot(211)
    c = report['codes']
    ax.plot(c[0], 'b--')
    ax.plot(c[1], 'r--')
    ax.set_title('Codes vs Event Number')
    ax = plt.subplot(212)
    d = report['diffs']
    ax.plot(d[0], 'b--')
    ax.plot(d[1], 'r--')
    ax.set_title('SOA vs Event Number')
    plt.show()


def runfromfile(jsfile):
    with open(jsfile, 'r') as jsonfile:
        dirdict = json.load(jsonfile)

    for key in dirdict:
        print(key)
        for filepair in dirdict[key]:
            print('File Pair: ', filepair)
            if input('Run? (Y/N)') == 'Y':
                report = load_pair(*filepair)
                display(report)

if __name__ == '__main__':
    report = load_pair(sys.argv[1], sys.argv[2])
    display(report)
