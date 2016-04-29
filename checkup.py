# coding: utf-8
import os
import matplotlib.pyplot as plt
import pandas as pd
from prespy.logfile import load


logfiles = []
resp_classes = {'hit': 1, 'miss': 2, 'incorrect': 3}
lengths = {'LONG': 1, 'SHORT': 2}
deviant = {'EHD': 1, 'LD': 2, 'other': 3}


def loadem():
    for path in os.listdir('.'):
        if os.path.isfile(path) and path.endswith('.log'):
            logfiles.append(load(path))


def scatterem():
    for l in logfiles:
        soundevts = [e for e in l.events if e.etype == 'Sound']
        responses = [resp_classes[e.data['Stim Type']] for e in soundevts]
        plt.scatter(list(range(len(responses))), responses)
        plt.yticks(sorted(resp_classes.values()),
                   sorted(resp_classes, key=resp_classes.get))
        plt.title(l.subjectID)
        plt.show()

def classifyem():
    for l in logfiles:
        df = pd.DataFrame([e.data for e in l.events])
        df
