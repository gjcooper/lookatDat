# coding: utf-8
from prespy.logfile import load
import os, sys
import matplotlib.pyplot as plt
exp = dict(ifffi_home='test-ifffi.log', nss_home='testsoundtiming-nss.log', ps_home='testsoundtiming-timemmn.log',
        ifffi_lab='soundtest-ifffi.log', nss_lab='soundtest-nss.log', ps_lab='soundtest-ps-timemmn.log')

evts = dict(ifffi='ifffi_events.txt', nss='nss_events.txt', psr='psr_events.txt')


def examine(label, times):
    """examine the times (ie plot) and label it appropriately"""
    print('Examining time differences for ' + label)
    for t in times[:]:
        if t > 400:
            print('Large time diff of: ' + str(t) + ' found')
            times.remove(t)
    plt.hist(times)
    plt.title(label)
    plt.show()
    plt.plot(times)
    plt.title(label)
    plt.show()

    
def logfiles(lfdict):
    """examine each logfile in `lfdict`"""
    for e,i in lfdict.items():
        lf = load(i)
        snds = [ee.time for ee in lf.events if ee.etype == 'Sound']
        tdfs = [t-snds[x] for x,t in enumerate(snds[1:])]
        examine(e, tdfs)


def evtfiles(efdict):
    """examine each event file in `efdict`"""
    for e,i in efdict.items():
        with open(i, 'r') as efile:
            lines = efile.read().splitlines()
        nslist = ['254', '255']
        stimes = [int(ee.split()[3]) for ee in lines if ee.split()[7] not in nslist]
        tdfs = [t-stimes[x] for x,t in enumerate(stimes[1:])]
        examine(e, tdfs)

