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
    ecodes = [d.code for d in efile.events]
    for c in pcodes[:]:
        try:
            int(c)
        except ValueError:
            print('Warning: Non-number code found, cannot plot', c)
            pcodes.remove(c)
    # load time differences between events
    ptimes = [e.time for e in pfile.events]
    etimes = [float(d.time) for d in efile.events]
    pdiffs = [t - ptimes[i] for i, t in enumerate(ptimes[1:])]
    ediffs = [(t - etimes[i])*1000 for i, t in enumerate(etimes[1:])]
    # Return report
    return dict(codes=(pcodes, ecodes), diffs=(pdiffs, ediffs), times=(ptimes, etimes))

def filter_by_large(label, data, acceptrange):
    warnings = ['{0:<9}{1:>7}{2:>12}{3!s:>12}'.format('Label', 'EvtNum', 'Value', 'Range')]
    for i, d in enumerate(data[:]):
        if d < acceptrange[0] or d > acceptrange[1]:
            data.remove(d)
            warnings.append('{0:<9}{1:>7}{2:>12.1f}{3!s:>12}'.format(label, i, d, acceptrange))
    if len(warnings) == 1:
        return data
    if input(str(len(warnings)-1) + ' warnings found: Print?(Y/N)') == 'Y':
        print('\n'.join(warnings))
    return data

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
    ax.plot(filter_by_large('logdiffs', d[0], (290, 310)), 'b--')
    ax.plot(filter_by_large('evtdiffs', d[1], (290, 310)), 'r--')
    ax.set_title('SOA vs Event Number')
    plt.show()


def runfromfile(jsfile):
    with open(jsfile, 'r') as jsonfile:
        dirdict = json.load(jsonfile)

    for key in dirdict:
        print(key)
        for filepair in dirdict[key]:
            print('File Pair: ', filepair)
            if input('Skip? (Y/N)') != 'Y':
                report = load_pair(*filepair)
                display(report)

if __name__ == '__main__':
    report = load_pair(sys.argv[1], sys.argv[2])
    display(report)
