import os

import matplotlib.pyplot as plt
import numpy as np
from dotmap import DotMap


def make_repetitionsummary_figures(allsimparams ,metaparams):

    axesdims = DotMap()
    axesdims.figFinalWeights.x1 = 0.1
    axesdims.figFinalWeights.w1 = 0.8
    axesdims.figFinalWeights.y1 = 0.05
    axesdims.figFinalWeights.h1 = 0.9

    for simparams in allsimparams:
        print "Drawing final-weights figure for psim '"+ simparams.extendedparamFoldername + "'"
        figFinalWeights = plt.figure(figsize=(6, 12))
        plotFinalWeights(axesdims, simparams, metaparams)
        imagename = metaparams.figures_basename + '_FinalWeights.png'
        figFinalWeights.savefig(metaparams.figures_path + simparams.extendedparamFoldername + '/' + imagename)
        plt.close(figFinalWeights)

    pass

    make_repetitionsummary_html(allsimparams, metaparams, imagename)


def make_repetitionsummary_html(allsimparams, metaparams, imagename):
    htmlfile = open(metaparams.figures_path + '/repetitionsummaries.html', 'w')

    htmlfile.write('<html> \n')
    htmlfile.write('<body> \n')
    htmlfile.write('<table><tr> \n')

    for simparams in allsimparams:
        imglink = simparams.extendedparamFoldername + '/' + imagename
        htmlfile.write('<td><img src=' + imglink + ' /></td>')

    htmlfile.write('</tr></table> \n')
    htmlfile.write('</body> \n')
    htmlfile.write('</html> \n')
    htmlfile.close()






def plotFinalWeights(axesdims, simparams, metaparams):
    newlocation = [axesdims.figFinalWeights.x1, axesdims.figFinalWeights.y1, axesdims.figFinalWeights.w1,
                   axesdims.figFinalWeights.h1]
    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title='final weights (' + str(metaparams.numRepetitions) + ' repetitions)')

    finalweights = readFinalWeights(simparams, metaparams)

    # plt.imshow(weightdevelopment.T, aspect='auto',extent=[extent_left,extent_right,extent_bottom,extent_top],interpolation='none')
    plt.imshow(finalweights.T, aspect='auto', interpolation='none')
    ylims = plt.ylim()
    plt.ylim((ylims[1], ylims[0]))
    # plt.clim(0,1)
    # thecolorbar = plt.colorbar()
    # thecolorbar.set_label('synaptic strength (weight)')

    xsize = finalweights.shape[0]
    ysize = finalweights.shape[1]
    plt.text(0 - 0.5, ysize * 1.04, simparams.extendedparamFoldername, ha='left', va='center')
    plt.text(metaparams.numRepetitions - 0.5, ysize * -0.04, simparams.extendedparamFoldername, ha='right', va='center')
    # plt.text(metaparams.numRepetitions/2.0, 600, str(finalweights.shape),ha='center',va='center')

    repIDs = np.arange(metaparams.numRepetitions)
    plt.xticks(repIDs, repIDs + 1)

    pass


def readFinalWeights(simparams, metaparams):
    finalweights = np.zeros([metaparams.numRepetitions, simparams.neurongroups.inputs.N])

    for repetitionID in xrange(metaparams.numRepetitions):
        repfolder = metaparams.repetitionFoldernames[repetitionID]
        os.system('mkdir -p ' + metaparams.figures_path + simparams.extendedparamFoldername)

        weightssummaryfilename = metaparams.data_path + simparams.extendedparamFoldername + '/' + repfolder + '/' + metaparams.figures_basename + '.weightmatrix'
        simdata = np.genfromtxt(weightssummaryfilename,
                                names="time,mean,std,timestepfilename",
                                comments='#',  # skip comment lines
                                dtype=None
                                )  # guess dtype of each column

        numSnapshots = len(simdata)
        # timeaxis = simdata['time']
        # print finalweights.shape
        # for i in xrange(numSnapshots):

        i = numSnapshots - 1
        weightdata = np.genfromtxt(metaparams.data_path + simparams.extendedparamFoldername + '/' + repfolder + '/' +
                                   simdata['timestepfilename'][i],
                                   names="preID,postID,weight",
                                   skip_header=6,
                                   comments='%',  # skip comment lines
                                   dtype=None)  # guess dtype of each column
        finalweights[repetitionID, weightdata['preID'] - 1] = weightdata['weight']

    return finalweights
