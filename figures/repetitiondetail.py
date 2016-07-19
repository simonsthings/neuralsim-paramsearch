import numpy as np
import dotmap
import os
import matplotlib.pyplot as plt
from numpy import int32, arange
import peakutils


def make_singlerun_figures(allsimparams, metaparams):
    axesdims = dotmap.DotMap()
    axesdims.figSpikes.x = 0.1
    axesdims.figSpikes.w = 0.85
    axesdims.figSpikes.y1 = 0.75 # input raster
    axesdims.figSpikes.h1 = 0.2  # input raster
    axesdims.figSpikes.y2 = 0.25 # membranes
    axesdims.figSpikes.h2 = 0.1  # membranes
    axesdims.figSpikes.y3 = 0.1  # output raster
    axesdims.figSpikes.h3 = 0.05 # output rater
    axesdims.figSpikes.y4 = 0.4  # ampa
    axesdims.figSpikes.h4 = 0.1  # ampa
    axesdims.figSpikes.y5 = 0.55 # nmda
    axesdims.figSpikes.h5 = 0.1  # nmda

    axesdims.figWeights.x1 = 0.1
    axesdims.figWeights.w1 = 0.9
    axesdims.figWeights.x2 = None  # will be set below!
    axesdims.figWeights.w2 = None  # will be set below!
    axesdims.figWeights.x3 = 0.86
    axesdims.figWeights.w3 = 0.05

    ps = 0.12
    axesdims.figWeights.y2 = 0.41 + ps  # rate
    axesdims.figWeights.h2 = 0.05  # rate
    axesdims.figWeights.y3 = 0.51 + ps  # stats!
    axesdims.figWeights.h3 = 0.05  # stats!
    axesdims.figWeights.y4 = 0.05  # responses
    axesdims.figWeights.h4 = 0.30 + ps  # responses
    axesdims.figWeights.y1 = 0.6 + ps  # weights
    axesdims.figWeights.h1 = axesdims.figWeights.h4 / 2.0 * 700.0 / 600.0  # 0.35  # weights

    # nestedPrint(axesdims)
    developmentfigname = metaparams.figures_basename + '_WeightsDevelopment'

    for simparams in allsimparams:
        print "Drawing weight development figures for folder " + simparams.extendedparamFoldername + "."
        for repetitionID in xrange(metaparams.numRepetitions):
            # for repetitionID in xrange(2):
            repfolder = metaparams.repetitionFoldernames[repetitionID]
            os.system('mkdir -p ' + metaparams.figures_path + simparams.extendedparamFoldername + '/' + repfolder)

            # print "Drawing weight development figure for repetition "+str(repetitionID)+" in folder "+simparams.extendedparamFoldername+"."
            figWeightsDevelopment = plt.figure(figsize=(9, 11))
            if False:
                weightdata = readWeightsFromFiles(simparams, metaparams, repfolder)
                (axBounds, axXlim) = plotWeights(axesdims, simparams, weightdata)
                axesdims.figWeights.x2 = axBounds[0]
                axesdims.figWeights.w2 = axBounds[2]
                plotWeightTraces(axesdims, simparams, weightdata)
            else:
                axesdims.figWeights.x2 = axesdims.figWeights.x1
                axesdims.figWeights.w2 = 0.75
                axXlim = None
            plotResponses(axesdims, simparams,
                          metaparams.data_path + simparams.extendedparamFoldername + '/' + repfolder + '/' + metaparams.figures_basename,
                          timespan=axXlim)
            plotResponseHistograms(axesdims, simparams,
                                   metaparams.data_path + simparams.extendedparamFoldername + '/' + repfolder + '/' + metaparams.figures_basename,
                                   timespan=axXlim)
            plotOutputrate(axesdims, simparams,
                           metaparams.data_path + simparams.extendedparamFoldername + '/' + repfolder + '/' + metaparams.figures_basename,
                           timespan=axXlim)
            # plotWeightstatistics(axesdims,simparams,metaparams.data_path+simparams.extendedparamFoldername+'/'+repfolder+'/'+metaparams.figures_basename,timespan=axXlim)
            figWeightsDevelopment.savefig(
                metaparams.figures_path + simparams.extendedparamFoldername + '/' + repfolder + '/' + developmentfigname + '.png')
            # figWeightsDevelopment.savefig(metaparams.figures_path+simparams.extendedparamFoldername+'/'+repfolder+'/'+developmentfigname+'.pdf')
            plt.close(figWeightsDevelopment)

    # simdata = getSimData(metaparams.data_path+simparams.extendedparamFoldername+'/'+repfolder+'/'+metaparams.figures_basename)
    #         for mi in xrange(len(simparams.recordings.dtintervalsAsFloats.starttimes)):
    #             starttime = simparams.recordings.dtintervalsAsFloats.starttimes[mi]
    #             stoptime = simparams.recordings.dtintervalsAsFloats.stoptimes[mi]
    #             timespan = (starttime,stoptime)  # seconds
    #             print "Now drawing membrane and raster plot figure for timespan " + str(timespan) + ""
    #             figSpikesAndMembranes = plt.figure()
    #             inputraster(axesdims,simdata,timespan)
    #             membranes(axesdims,simdata,timespan)
    #             ampa(axesdims,simdata,timespan)
    #             #nmda(axesdims,simdata,timespan)
    #             outputraster(axesdims,simdata,timespan)
    #             figSpikesAndMembranes.savefig(metaparams.figures_path+simparams.extendedparamFoldername+'/'+repfolder+'/'+metaparams.figures_basename+'_SpikesAndMembranes_start'+str(starttime)+'s.png')
    #             #plt.show() ; exit()
    #             plt.close(figSpikesAndMembranes)
    #

    make_singleruns_html(allsimparams, metaparams, developmentfigname)


def make_singleruns_html(allsimparams, metaparams, imagename):
    htmlfile = open(metaparams.figures_path + '/responsedevelopment.html', 'w')

    htmlfile.write('<html> \n')
    htmlfile.write('<body> \n')
    htmlfile.write('<table> \n')

    # write column headers:
    htmlfile.write('<tr><th></th> \n')
    for simparams in allsimparams:
        htmlfile.write('<th>' + simparams.extendedparamFoldername.replace('_',' ') + '</th> \n')
    htmlfile.write('</tr> \n')

    for repetitionID in xrange(metaparams.numRepetitions):
        repfolder = metaparams.repetitionFoldernames[repetitionID]
        htmlfile.write('<tr> \n')
        # write row headers:
        htmlfile.write('<th>Repetition_' + str(repetitionID + 1) + '</th> \n')

        for simparams in allsimparams:
            imglink = simparams.extendedparamFoldername + '/' + repfolder + '/' + imagename + '.png'
            imgtag = '<img width=150px src=' + imglink + ' />'
            htmlfile.write('<td><a href=' + imglink + '>' + imgtag + '</a></td> \n')

        htmlfile.write('</tr> \n')

    htmlfile.write('</table> \n')
    htmlfile.write('</body> \n')
    htmlfile.write('</html> \n')
    htmlfile.close()








def getSingleDatatrail(filename, columnNames):
    if os.path.isfile(filename) and os.path.getsize(filename) > 0:
        try:
            datatrail = np.genfromtxt(filename,
                                      names=columnNames,
                                      comments='#',  # skip comment lines
                                      dtype=None)  # guess dtype of each column
        except Exception as e:
            print "Oh-oh! There was an exception: " + str(e)
            print "The type of it was: " + str(type(e))
            exit()
    else:
        if not os.path.isfile(filename):
            print "The file '" + filename + "' does not exist. Skipping."
        else:
            print "The file '" + filename + "' is empty. Skipping."
        datatrail = []

    return datatrail


def getSimData(datafile_basename):
    simdata = {}
    simdata['input_raster'] = getSingleDatatrail(datafile_basename + '_inputs.ras', "time,nodeID")
    simdata['output_raster'] = getSingleDatatrail(datafile_basename + '_outputs.ras', "time,nodeID")
    simdata['membranes'] = getSingleDatatrail(datafile_basename + '.mem', "time,mempot")
    simdata['ampa'] = getSingleDatatrail(datafile_basename + '.ampa', "time,ampa")
    simdata['nmda'] = getSingleDatatrail(datafile_basename + '.nmda', "time,nmda")
    return simdata


def membranes(axesdims, theSimdata, timespan=None):
    datatrail = theSimdata['membranes']

    newlocation = [axesdims.figSpikes.x, axesdims.figSpikes.y2, axesdims.figSpikes.w, axesdims.figSpikes.h2]
    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title='membrane potentials')

    # Crop large membranes:
    datatrail['mempot'][datatrail['mempot'] > 30] = 30

    # print(simdata)
    if timespan:
        indexes = (datatrail['time'] > timespan[0]) & (datatrail['time'] < timespan[1])
        plt.plot(datatrail['time'][indexes], datatrail['mempot'][indexes])
        # plt.plot(datatrail[-1000:,0],datatrail[-1000:,1],'-')
    else:
        plt.plot(datatrail['time'], datatrail['mempot'])

    if timespan:
        plt.xlim(timespan)
    # theYLims = plt.ylim()
    # plt.ylim([-0.08,0.04])
    # plt.ylim([-0.04,0.12])
    # plt.ylim([-0.02,0.1])

    theYticks = ax.get_yticks()
    newYticks = [theYticks[0], theYticks[-1]]
    ax.set_yticks(newYticks)


def ampa(axesdims, theSimdata, timespan=None):
    datatrail = theSimdata['ampa']

    newlocation = [axesdims.figSpikes.x, axesdims.figSpikes.y4, axesdims.figSpikes.w, axesdims.figSpikes.h4]
    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title='summed inputs ("ampa")')

    # print(simdata)
    if timespan:
        indexes = (datatrail['time'] > timespan[0]) & (datatrail['time'] < timespan[1])
        plt.plot(datatrail['time'][indexes], datatrail['ampa'][indexes])
        # plt.plot(datatrail[-1000:,0],datatrail[-1000:,1],'-')
    else:
        plt.plot(datatrail['time'], datatrail['mempot'])

    if timespan:
        plt.xlim(timespan)
    # plt.ylim([-0.08,0.04])

    theYticks = ax.get_yticks()
    newYticks = [theYticks[0], theYticks[-1]]
    ax.set_yticks(newYticks)


def nmda(axesdims, theSimdata, timespan=None):
    datatrail = theSimdata['nmda']

    newlocation = [axesdims.figSpikes.x, axesdims.figSpikes.y5, axesdims.figSpikes.w, axesdims.figSpikes.h5]
    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title='nmda')

    # print(simdata)
    if timespan:
        indexes = (datatrail['time'] > timespan[0]) & (datatrail['time'] < timespan[1])
        plt.plot(datatrail['time'][indexes], datatrail['nmda'][indexes])
        # plt.plot(datatrail[-1000:,0],datatrail[-1000:,1],'-')
    else:
        plt.plot(datatrail['time'], datatrail['mempot'])

    if timespan:
        plt.xlim(timespan)
    # plt.ylim([-0.08,0.04])

    theYticks = ax.get_yticks()
    newYticks = [theYticks[0], theYticks[-1]]
    ax.set_yticks(newYticks)


def inputraster(axesdims, theSimdata, timespan=None):
    datatrail = theSimdata['input_raster']

    newlocation = [axesdims.figSpikes.x, axesdims.figSpikes.y1, axesdims.figSpikes.w, axesdims.figSpikes.h1]
    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title='input spike raster')

    if timespan:
        indexes = (datatrail['time'] > timespan[0]) & (datatrail['time'] < timespan[1])
        plt.plot(datatrail['time'][indexes], datatrail['nodeID'][indexes], '.k')
        # plt.plot(datatrail[-1000:,0],datatrail[-1000:,1],'-')
        plt.xlim(timespan)
    else:
        plt.plot(datatrail['time'], datatrail['nodeID'], '.k')
    plt.ylim([0, 700])


def outputraster(axesdims, theSimdata, timespan=None):
    datatrail = theSimdata['output_raster']

    newlocation = [axesdims.figSpikes.x, axesdims.figSpikes.y3, axesdims.figSpikes.w, axesdims.figSpikes.h3]
    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title='output spike raster')

    if type(datatrail) is list or datatrail.size == 0:
        print "There are no output spikes to print. Skipping the output spike raster plot of this figure."
        plt.title('no output spikes')
        return

    if timespan:
        indexes = (datatrail['time'] > timespan[0]) & (datatrail['time'] < timespan[1])
    else:
        indexes = np.arange(len(datatrail))
        # plt.plot(datatrail['time'],datatrail['nodeID'],'.k')
    plt.plot(datatrail['time'][indexes], datatrail['nodeID'][indexes], '.k')

    if timespan:
        plt.xlim(timespan)
    else:
        pass
    ax.set_xlabel('time (s)');

    theYticks = ax.get_yticks()
    newYticks = [theYticks[0], theYticks[-1]]
    ax.set_yticks(newYticks)






def plotWeights(axesdims, simparams, weightdata):
    # (timeaxis,weightdevelopment) = readWeightsFromFiles(simparams,sim_data_path,sim_data_basename)
    (timeaxis, weightdevelopment) = weightdata

    newlocation = [axesdims.figWeights.x1, axesdims.figWeights.y1, axesdims.figWeights.w1, axesdims.figWeights.h1]
    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title='weight development over time')
    # print ax.get_position().bounds

    extent_x_overlap = (timeaxis[1] - timeaxis[0]) / 2
    extent_y_overlap = 0.5  # because here we don't need specific rescaling and just want the # of rows.
    extent_left = timeaxis[0] - extent_x_overlap
    extent_right = timeaxis[-1] + extent_x_overlap
    extent_bottom = weightdevelopment.shape[1] - 1 + extent_y_overlap
    extent_top = 0 - extent_y_overlap
    plt.imshow(weightdevelopment.T, aspect='auto', extent=[extent_left, extent_right, extent_bottom, extent_top],
               interpolation='none')
    # plt.clim(0,1)
    thecolorbar = plt.colorbar()
    thecolorbar.set_label('synaptic strength (weight)')

    plt.ylabel('presyn. units (#)')

    # print ax.get_position().bounds
    # print plt.xlim()
    # print "Weights-YLim: " + str(plt.ylim())
    plt.ylim(-0.5, 699.5)
    # plt.ylim(-0.5,1199.5)

    ax.set_xticks([])

    return (ax.get_position().bounds, plt.xlim())


def plotWeightTraces(axesdims, simparams, weightdata):
    (timeaxis, weightdevelopment) = weightdata

    newlocation = [axesdims.figWeights.x2, axesdims.figWeights.y3, axesdims.figWeights.w2, axesdims.figWeights.h3]
    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title='weight development over time')
    # print ax.get_position().bounds

    strongIDs = weightdevelopment[-1, :] > 0.9

    strongweights = weightdevelopment[:, strongIDs]
    weakweights = weightdevelopment[:, strongIDs == False]

    plt.plot(timeaxis, weakweights, 'b')
    if strongIDs.sum() > 0:
        plt.plot(timeaxis, strongweights, 'r')

    # plt.plot(timeaxis,weightdevelopment[ : , -1:0:-1 ])
    # plt.clim(0,1)

    plt.ylabel('weights (a.u.)')

    # plt.ylim(0.0,1.0)

    ax.set_yticks([0, 1])
    # ax.set_xticks([])


def readWeightsFromFiles(simparams, metaparams, repfolder):
    print "Reading weight snapshots..."
    weightssummaryfilename = metaparams.data_path + simparams.extendedparamFoldername + '/' + repfolder + '/' + metaparams.figures_basename + '.weightmatrix'
    print weightssummaryfilename
    simdata = np.genfromtxt(weightssummaryfilename,
                            names="time,mean,std,timestepfilename",
                            comments='#',  # skip comment lines
                            dtype=None
                            )  # guess dtype of each column

    numSnapshots = len(simdata)
    timeaxis = simdata['time']
    weightdevelopment = np.zeros([numSnapshots, simparams.neurongroups.inputs.N])
    # print weightdevelopment.shape
    # for i in xrange(4):
    for i in xrange(numSnapshots):
        # print timesteptuple
        weightdata = np.genfromtxt(metaparams.data_path + simparams.extendedparamFoldername + '/' + repfolder + '/' +
                                   simdata['timestepfilename'][i],
                                   names="preID,postID,weight",
                                   skip_header=6,
                                   comments='%',  # skip comment lines
                                   dtype=None)  # guess dtype of each column
        if i % 50 == 0:
            print "Reading weights of time " + str(simdata['time'][i]) + " from file '" + simdata['timestepfilename'][
                i] + "' (snapshot " + str(i + 1) + "/" + str(numSnapshots) + ")"
        weightdevelopment[i, weightdata['preID'] - 1] = weightdata['weight']
        # weightdevelopment[i,:] = weightdata['weight']
    print "Finished reading weight snapshots!"
    return (timeaxis, weightdevelopment)


def plotOutputrate(axesdims, simparams, datafile_basename, timespan=None):
    newlocation = [axesdims.figWeights.x2, axesdims.figWeights.y2, axesdims.figWeights.w2, axesdims.figWeights.h2]
    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title="output neuron's (sliding average) rate")
    simdata = np.genfromtxt(datafile_basename + '_outputs.rate',
                            names="time,rate",
                            comments='#',  # skip comment lines
                            dtype=None)  # guess dtype of each column

    # print(simdata)
    if timespan:
        indexes = (simdata['time'] > timespan[0]) & (simdata['time'] < timespan[1])
    else:
        indexes = np.arange(len(simdata))
    plt.fill_between(simdata['time'][indexes], simdata['rate'][indexes])

    if timespan:
        plt.xlim(timespan)
    else:
        pass
    plt.ylabel('rate (Hz)')

    theYlim = plt.ylim()
    # print "The Y lim: " + str(theYlim)
    scaledata = simdata['rate'][indexes]
    scalestart_at_second = 10
    scalestart_at_index = int(scalestart_at_second / simparams.recordings.outputs.samplinginterval_rate)
    # print scalestart_at_index
    # print scaledata.shape
    theYmax = scaledata[scalestart_at_index:-1].max()
    # print theYmax
    plt.ylim([theYlim[0], theYmax])

    theYticks = ax.get_yticks()
    newYticks = [theYticks[0], theYticks[-1]]
    ax.set_yticks(newYticks)

    ax.set_xticks([])


def plotResponses(axesdims, simparams, datafile_basename, timespan=None):
    newlocation = [axesdims.figWeights.x2, axesdims.figWeights.y4, axesdims.figWeights.w2, axesdims.figWeights.h4]
    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title="output neuron's responses relative to pattern onset")

    fname = datafile_basename + '_outputs.spk'
    thedatatype = np.dtype([('time', int32), ('neuronID', int32)])
    # print "Now loading data!"
    simdata = np.fromfile(fname, dtype=thedatatype)
    # print "Finished loading the data!"
    # print "Size of array: " + str(simdata.shape)
    # print "Type of array: " + str(type(simdata))
    # print "Contents of array: " + str(simdata)

    stepspersecond = simdata['time'][0]
    # print "Steps per second: " + str(stepspersecond)
    dt = 1.0 / stepspersecond
    # print " -> stepsize: " + str(dt)



    # simtime = 400 # seconds

    denseSpiketimes = np.zeros(simparams.general.simtime * stepspersecond)

    endplot = -1
    # endplot = 100000
    denseSpiketimes[simdata['time'][1:endplot]] = 1

    #     #print denseSpiketimes.shape
    #     patterninterval = 0.2 # 200 ms
    #     #denseSpiketimes.reshape((stepspersecond*patterninterval,-1))
    #     #np.reshape(denseSpiketimes,(stepspersecond*patterninterval,-1))
    #     #np.reshape(denseSpiketimes,(200,-1))
    denseSpiketimes = denseSpiketimes.reshape((-1, int(stepspersecond * simparams.neurongroups.inputs.patterninterval) ))
    # print denseSpiketimes.shape

    xmin = 0
    xmax = simparams.general.simtime
    yloc = simparams.neurongroups.inputs.patternduration * 1000
    plt.plot([xmin, xmax], [yloc, yloc], '--', color='gray')

    (rows, cols) = np.nonzero(denseSpiketimes)
    plt.plot(rows * simparams.neurongroups.inputs.patterninterval, cols * dt * 1000.0, '.k')
    # plt.plot(rows*dt*1000,cols*simparams.neurongroups.inputs.patterninterval,'.')
    plt.ylabel('time (ms)')

    plt.xlabel('time (s)')


def plotResponseHistograms(axesdims, simparams, datafile_basename, timespan=None):
    newlocation = [axesdims.figWeights.x3, axesdims.figWeights.y4, axesdims.figWeights.w3, axesdims.figWeights.h4]
    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title="peaks")

    fname = datafile_basename + '_outputs.spk'
    thedatatype = np.dtype([('time', int32), ('neuronID', int32)])
    simdata = np.fromfile(fname, dtype=thedatatype)

    stepspersecond = simdata['time'][0]
    dt = 1.0 / stepspersecond
    denseSpiketimes = np.zeros(simparams.general.simtime * stepspersecond)
    endplot = -1
    # endplot = 100000
    denseSpiketimes[simdata['time'][1:endplot]] = 1

    useLastXFractionOfData = 3.0 / 4.0;
    # nestedPrint(simparams )

    denseSpiketimes = denseSpiketimes.reshape((-1, int(stepspersecond * simparams.neurongroups.inputs.patterninterval) ))
    responseHistogram = (denseSpiketimes[int(denseSpiketimes.shape[0] * useLastXFractionOfData):, :]).sum(axis=0)
    # print "denseSpiketimes.sum: " + str( responseHistogram )

    # print "responseHistogram[0:20]: " + str(responseHistogram[0:20])
    # print "Sum: " + str(responseHistogram.sum())

    timeduringtest = simparams.general.simtime * (1 - useLastXFractionOfData)
    # print "timeduringtest: " + str(timeduringtest)
    patternsPerSecond = 1 / (simparams.neurongroups.inputs.patterninterval)
    # print "patternsPerSecond: " + str(patternsPerSecond)
    patternPresentationsDuringTestTimespan = timeduringtest * patternsPerSecond
    # print "patternPresentationsDuringTestTimespan: " + str(patternPresentationsDuringTestTimespan)
    if responseHistogram.sum() < patternPresentationsDuringTestTimespan / 10.0:
        # print "Not enough activity to compute peaks! Skipping."
        plt.text(0.5, 0.5, "Not enough activity for peaks.", rotation=90, va="center", ha="center")
        ##return
    else:
        # introduce some randomness so that the peakutils.indexes() method doesn't get confused by two equal values!
        # responseHistogram += np.random.randn(responseHistogram.size) * 0.0001
        responseHistogram += arange(responseHistogram.size, 0, -1) * 0.000001

        the_min_dist = 3
        dt_correction = 1e-3 / dt
        indexes = peakutils.indexes(responseHistogram, thres=0.3, min_dist=the_min_dist * dt_correction)  # *1e-3/dt
        # print "The indices are:"
        # print indexes
        ##print "The values at the found positions:"
        ##print responseHistogram[indexes]

        numstrings = ["st: ", "nd: ", "rd: ", "th: "]
        ## plot peaks:
        ##for index in indexes:
        for ii in xrange(len(indexes)):
            index = indexes[ii]
            plt.plot(responseHistogram[index], index / dt_correction, 'or', markersize=5, fillstyle='none')
            if ii < 4:
                numstring = numstrings[ii];
            else:
                numstring = numstrings[3]
            plt.text(max(responseHistogram) * 1.2, index / dt_correction,
                     str(ii + 1) + numstring + str(index / dt_correction) + "ms", verticalalignment='center')

        # plot actual histogram
        plt.fill_between(responseHistogram, 0, arange(responseHistogram.size) / dt_correction)
        # plt.plot( responseHistogram , arange(responseHistogram.size)/dt_correction )

        plt.xlim([0, max(responseHistogram) * 1.1])

    ax.set_xticks([])
    ax.set_yticks([])
    plt.xlabel('#')


def plotWeightstatistics(axesdims, simparams, datafile_basename, timespan=None):
    newlocation = [axesdims.figWeights.x2, axesdims.figWeights.y3, axesdims.figWeights.w2, axesdims.figWeights.h3]
    fig = plt.gcf()
    ax = fig.add_axes(newlocation, title="output neuron's weight stats")
    simdata = np.genfromtxt(datafile_basename + '.weightstats',
                            names="time,mean,std",
                            comments='#',  # skip comment lines
                            dtype=None)  # guess dtype of each column

    # print(simdata)
    if timespan:
        indexes = (simdata['time'] > timespan[0]) & (simdata['time'] < timespan[1])
    else:
        indexes = np.arange(len(simdata))
    plt.plot(simdata['time'][indexes], simdata['mean'][indexes])
    # plt.plot(simdata['time'][indexes],simdata['std'][indexes])

    if timespan:
        plt.xlim(timespan)
    else:
        pass
    plt.ylabel('mean weight')
    # plt.ylabel('mean,std')


    theYlim = plt.ylim()
    # print "The Y lim: " + str(theYlim)
    scaledata = simdata['mean'][indexes]
    # scaledata = simdata['std'][indexes]
    scalestart_at_second = 10
    scalestart_at_index = scalestart_at_second / simparams.recordings.outputs.samplinginterval_rate
    # print scalestart_at_index
    # print scaledata.shape
    theYmax = scaledata[scalestart_at_index:-1].max()
    # print theYmax
    plt.ylim([theYlim[0], theYmax])

    theYticks = ax.get_yticks()
    newYticks = [theYticks[0], theYticks[-1]]
    ax.set_yticks(newYticks)

    ax.set_xticks([])

