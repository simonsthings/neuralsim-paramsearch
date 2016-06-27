import numpy as np
import dotmap
import matplotlib.pyplot as plt
from numpy import arange




def make_overview_figures(allsimparams ,metaparams):

    print "Making Overview figures..."
    axesdims = dotmap.DotMap()
    fs = (8 ,10)
    location1 = [0.1 ,0.45 ,0.28 ,0.45]
    location2 = [0.55 ,0.45 ,0.28 ,0.45]
    location3 = [0.1 ,0.09 ,0.5 ,0.2]
    location4 = [0.7 ,0.09 , 0.2 /fs[0 ] *fs[1] ,0.2]

    numParamsTested = len(allsimparams[0].extendedparams)
    print "numParamsTested: " + str(numParamsTested)
    if numParamsTested > 1:
        paramToShow = 'projMul'

    paramFullPath = allsimparams[0].extendedparams.keys()[0]
    # shortPrarmStringID = paramFullPath.rfind('.')
    # shortParamString = paramFullPath[shortPrarmStringID+1:]

    figAccuracies = plt.figure(figsize=fs)
    plotAccuracies_param1_Repetitions(location1, allsimparams, metaparams, 'tpr', paramFullPath)
    plotAccuracies_param1_Repetitions(location2, allsimparams, metaparams, 'fpr', paramFullPath)
    plotTPRvsFPR_projMult(location3, allsimparams, metaparams, paramFullPath)
    plotROC_projMult(location4, allsimparams, metaparams)
    figAccuracies.savefig(metaparams.figures_path + metaparams.figures_basename + '_Accuracies_projMult_Repetition.png')
    plt.close(figAccuracies)

    pass




def plotAccuracies_param1_Repetitions(newlocation, allsimparams, metaparams, columnToUse, paramPathString):
    from helpers.parameters import getParamRecursively

    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title='final ' + str(columnToUse) + ' (x' + str(metaparams.numRepetitions) + ')')

    y_labels = []
    true_positive_rates = np.zeros((len(allsimparams), metaparams.numRepetitions));
    for sid in xrange(len(allsimparams)):
        simparams = allsimparams[sid]

        # print "projMult: " + str(simparams.neurongroups.outputs.projMult)
        paramValue = getParamRecursively(paramPathString, simparams)
        y_labels.append(paramValue)

        for repetitionID in xrange(metaparams.numRepetitions):
            repfolder = metaparams.repetitionFoldernames[repetitionID]

            stimdetfilename = metaparams.data_path + simparams.extendedparamFoldername + '/' + repfolder + '/' + metaparams.figures_basename + '.stimulusdetectionstatistics.txt'
            simdata = np.genfromtxt(stimdetfilename,
                                    # names="time,tpr,fpr,t_div_f",
                                    names="tpr,fpr,t_div_f",
                                    comments='#',  # skip comment lines
                                    dtype=None
                                    )  # guess dtype of each column

            numSnapshots = len(simdata)

            # print simdata[columnToUse]
            true_positive_rates[sid, repetitionID] = simdata[columnToUse][-1];
            # true_positive_rates[sid, repetitionID] = simdata['tpr'][-1];

    plt.imshow(true_positive_rates, aspect='auto', interpolation='nearest')
    # plt.colorbar()
    plt.clim(0, 1)

    theXticks = arange(metaparams.numRepetitions)
    plt.xticks(theXticks, theXticks + 1)
    plt.yticks(np.r_[0:len(y_labels)], y_labels)

    plt.xlabel('repetitions')
    paramShortID = paramPathString.rfind('.')
    paramShortString = paramPathString[paramShortID + 1:]
    plt.ylabel(paramShortString)

    # now show the means:

    meanlocation = newlocation
    meanlocation[0] = newlocation[0] + newlocation[2] + 0.02
    meanlocation[2] = newlocation[2] / metaparams.numRepetitions
    ax2 = fig.add_axes(meanlocation, title='mean')

    meanSomethingRates = true_positive_rates.mean(axis=1)
    plt.imshow(np.expand_dims(meanSomethingRates, axis=1), aspect='auto')
    plt.xticks([])
    plt.yticks([])
    pass


def plotTPRvsFPR_projMult(newlocation, allsimparams, metaparams, paramPathString):
    from helpers.parameters import getParamRecursively

    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title='final TPR vs. FPR over projMults')

    y_labels = []
    true_positive_rates = np.zeros((len(allsimparams), metaparams.numRepetitions));
    false_positive_rates = np.zeros((len(allsimparams), metaparams.numRepetitions));
    for sid in xrange(len(allsimparams)):
        simparams = allsimparams[sid]
        paramValue = getParamRecursively(paramPathString, simparams)
        y_labels.append(paramValue)

        for repetitionID in xrange(metaparams.numRepetitions):
            repfolder = metaparams.repetitionFoldernames[repetitionID]
            stimdetfilename = metaparams.data_path + simparams.extendedparamFoldername + '/' + repfolder + '/' + metaparams.figures_basename + '.stimulusdetectionstatistics.txt'
            simdata = np.genfromtxt(stimdetfilename,
                                    # names="time,tpr,fpr,t_div_f",
                                    names="tpr,fpr,t_div_f",
                                    comments='#',  # skip comment lines
                                    dtype=None
                                    )  # guess dtype of each column
            true_positive_rates[sid, repetitionID] = simdata['tpr'][-1];
            false_positive_rates[sid, repetitionID] = simdata['fpr'][-1];

    meanTPRs = true_positive_rates.mean(axis=1)
    meanFPRs = false_positive_rates.mean(axis=1)

    plt.plot(y_labels, meanTPRs)
    plt.plot(y_labels, meanFPRs)
    # plt.xticks(np.r_[0:len(y_labels)],y_labels)
    plt.ylim([-0.1, 1.1])
    paramShortID = paramPathString.rfind('.')
    paramShortString = paramPathString[paramShortID + 1:]
    plt.xlabel(paramShortString)
    plt.ylabel('tp or fp rate')


def plotROC_projMult(newlocation, allsimparams, metaparams):
    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title='ROC')

    y_labels = []
    true_positive_rates = np.zeros((len(allsimparams), metaparams.numRepetitions));
    false_positive_rates = np.zeros((len(allsimparams), metaparams.numRepetitions));
    for sid in xrange(len(allsimparams)):
        simparams = allsimparams[sid]
        y_labels.append(simparams.neurongroups.outputs.projMult)

        for repetitionID in xrange(metaparams.numRepetitions):
            repfolder = metaparams.repetitionFoldernames[repetitionID]
            stimdetfilename = metaparams.data_path + simparams.extendedparamFoldername + '/' + repfolder + '/' + metaparams.figures_basename + '.stimulusdetectionstatistics.txt'
            simdata = np.genfromtxt(stimdetfilename,
                                    # names="time,tpr,fpr,t_div_f",
                                    names="tpr,fpr,t_div_f",
                                    comments='#',  # skip comment lines
                                    dtype=None
                                    )  # guess dtype of each column
            true_positive_rates[sid, repetitionID] = simdata['tpr'][-1];
            false_positive_rates[sid, repetitionID] = simdata['fpr'][-1];

    meanTPRs = true_positive_rates.mean(axis=1)
    meanFPRs = false_positive_rates.mean(axis=1)

    plt.plot(meanFPRs, meanTPRs, '+')
    plt.xlabel('false positive rate')
    plt.ylabel('true positive rate')
    plt.xlim([-0.1, 1.1])
    plt.ylim([-0.1, 1.1])
    ax.tick_params(direction='out')
    plt.xticks([0, 0.5, 1.0])
    plt.yticks([0, 0.5, 1.0])



