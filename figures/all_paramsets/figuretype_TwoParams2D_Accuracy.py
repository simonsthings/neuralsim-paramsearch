import numpy as np
import dotmap
import matplotlib.pyplot as plt
from numpy import arange
import os
import helpers
from SimonsPythonHelpers import nestedPrint


def makeFig(params, paramdotpath):

	figtypename = 'OneParamAndRepetitions_Accuracy'

	print "Making figure type " + figtypename + " for parameter '" + paramdotpath + "'."

	#paramStringList = params.allsimparams[0].extendedparams.keys()
	paramStringList = params.flatParamLists.keys()


	#numParamsTested = len(allsimparams[0].extendedparams)
	#print "numParamsTested: " + str(numParamsTested)
	#if numParamsTested > 1:
	#    paramToShow = 'projMul'
	#for paramString in allsimparams[0].extendedparams:
	#    print paramString

	# paramdotpath = allsimparams[0].extendedparams.keys()[0]

	if paramdotpath in paramStringList:

		otherParamStringsList = list(paramStringList)
		otherParamStringsList.remove(paramdotpath)

		if otherParamStringsList: # if there are free parameters that require separate figures to be generated:
			groupedParamSets = helpers.parameters.splitByParameter(params.allsimparams,params.flatParamLists,otherParamStringsList)
			#print "The type of groupedParamSets is "+str(type(groupedParamSets))
			#nestedPrint(groupedParamSets,maxDepth=2)

			#nestedPrint(groupedParamSets,maxDepth=3)

			#print "Making figure for parameter '"+paramdotpath+"' and not for other parameters: "+ str(otherParamStringsList)


			# rearrange allsimparams into groups of otherparams with only varying values of paramdotpath:
			# do something for each value of each parameter except the given paramdotpath!
			# get subset of appsimparams where

			for paramGroupString in groupedParamSets.keys():
				paramSubgroup = groupedParamSets[paramGroupString]

				__doThePlotting(params, paramSubgroup, paramGroupString, paramdotpath,figtypename)

		else: # all parameter sets can be represented in a single figure:
			__doThePlotting(params, params.allsimparams, "theOnlyFigure", paramdotpath,figtypename)
	else:
		print "Skipping figure generation for param '" + paramdotpath + "' because this parameter was not found among the extended params lists."


def __doThePlotting(params, paramSubgroup, paramGroupString, paramFullPath,figtypename):

	metaparams = params.metaparams

	shortParamString = helpers.parameters.getDependentParameterShortNameString(params, paramFullPath)

	figBlob = figtypename + '_' + shortParamString
	figPath = metaparams.figures_path + 'figtype_' + figBlob + '/'
	os.system('mkdir -p ' + figPath)

	#axesdims = dotmap.DotMap()
	fs = (12 ,8)
	#location1 = [0.1 ,0.45 ,0.28 ,0.45]
	#location2 = [0.55 ,0.45 ,0.28 ,0.45]
	location1 = [0.1 ,0.75 ,0.65 ,0.2]
	location2 = [0.1 ,0.42 ,0.65 ,0.2]
	location3 = [0.1 ,0.09 ,0.65 ,0.2]
	location4 = [0.85 ,0.09 , 0.2 /fs[0 ] *fs[1] ,0.2]

	figAccuracies = plt.figure(figsize=fs)

	__plotAccuracies_param1_Repetitions(location1, paramSubgroup, metaparams, 'tpr', paramFullPath)
	__plotAccuracies_param1_Repetitions(location2, paramSubgroup, metaparams, 'fpr', paramFullPath)
	__plotTPRvsFPR_projMult(location3, paramSubgroup, metaparams, paramFullPath)
	__plotROC_projMult(location4, paramSubgroup, metaparams)

	figName = metaparams.figures_basename + '_' + figBlob + '__' + paramGroupString
	figAccuracies.savefig(figPath + figName + '.png')
	plt.close(figAccuracies)


def __plotAccuracies_param1_Repetitions(newlocation, allsimparams, metaparams, columnToUse, paramPathString):
	from helpers.parameters import getParamRecursively

	fig = plt.gcf()
	tprfprString = 'true positive rate'
	if columnToUse == 'fpr':
		tprfprString = 'false positive rate'

	ax = fig.add_axes(newlocation, title='(final) ' + tprfprString + ' (x' + str(metaparams.numRepetitions) + ')')

	x_ticklabels = []
	true_positive_rates = np.zeros((len(allsimparams), metaparams.numRepetitions));
	for sid in xrange(len(allsimparams)):
		simparams = allsimparams[sid]

		# print "projMult: " + str(simparams.neurongroups.outputs.projMult)
		paramValue = getParamRecursively(paramPathString, simparams)
		x_ticklabels.append(paramValue)

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

	plt.imshow(true_positive_rates.T, aspect='auto', interpolation='nearest')
	# plt.colorbar()
	plt.clim(0, 1)

	theYticks = arange(metaparams.numRepetitions)
	plt.yticks(theYticks, theYticks + 1)

	plt.ylabel('repetitions')
	paramShortID = paramPathString.rfind('.')
	paramShortString = paramPathString[paramShortID + 1:]
	plt.xlabel(paramShortString)
	plt.xticks(np.r_[0:len(x_ticklabels)], x_ticklabels)

	currentXTicks = plt.xticks()
	if len(x_ticklabels) > 10:
		idx = np.r_[1:len(x_ticklabels):round(len(x_ticklabels)/10)].astype(int)
		#print "idx: " + str(idx)
		for id in idx:
			currentXTicks[1][id]._text = ''
	plt.xticks( *currentXTicks)

	# now show the means:

	#meanlocation = list(newlocation)
	#meanlocation[0] = newlocation[0] + newlocation[2] + 0.02
	#meanlocation[2] = newlocation[2] / metaparams.numRepetitions
	#ax2 = fig.add_axes(meanlocation, title='mean')

	#meanSomethingRates = true_positive_rates.mean(axis=1)
	#plt.imshow(np.expand_dims(meanSomethingRates, axis=1), aspect='auto')
	#plt.xticks([])
	#plt.yticks([])
	pass


def __plotTPRvsFPR_projMult(newlocation, allsimparams, metaparams, paramPathString):
	from helpers.parameters import getParamRecursively

	fig = plt.gcf()
	lastax = plt.gca()
	ax = fig.add_axes(newlocation, title='final TPR vs. FPR over projMults')

	x_ticklabels = []
	true_positive_rates = np.zeros((len(allsimparams), metaparams.numRepetitions));
	false_positive_rates = np.zeros((len(allsimparams), metaparams.numRepetitions));
	for sid in xrange(len(allsimparams)):
		simparams = allsimparams[sid]
		paramValue = getParamRecursively(paramPathString, simparams)
		x_ticklabels.append(paramValue)

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
	stdTPRs = true_positive_rates.std(axis=1)
	stdFPRs = false_positive_rates.std(axis=1)

	# find useful min and max limits for the X axis:
	xmin = x_ticklabels[0] - (x_ticklabels[1]-x_ticklabels[0])/2.0
	xmax = x_ticklabels[-1] + (x_ticklabels[-1]-x_ticklabels[-2])/2.0

	plt.fill_between(x_ticklabels, meanTPRs+stdTPRs, meanTPRs-stdTPRs, color=(0,0,1,0.1),linewidth=0.0)
	plt.fill_between(x_ticklabels, meanFPRs+stdFPRs, meanFPRs-stdFPRs, color=(0,1,0,0.2),linewidth=0.0)

	plt.plot(x_ticklabels, meanTPRs, label='final true positive rate',linewidth=2.0)
	plt.plot(x_ticklabels, meanFPRs, label='final false positive rate',linewidth=2.0)
	plt.ylim([-0.1, 1.1])
	plt.xlim([xmin,xmax])
	paramShortID = paramPathString.rfind('.')
	paramShortString = paramPathString[paramShortID + 1:]
	plt.xlabel(paramShortString)
	plt.ylabel('tp or fp rate')
	plt.legend(fontsize=8, loc='center left')

	if len(x_ticklabels) > 10:
		idx = np.r_[0:len(x_ticklabels):round(len(x_ticklabels)/10)]
		#print "idx: " + str(idx)
		x_ticklabels = np.array(x_ticklabels)[idx.astype(int)]
	plt.xticks( x_ticklabels)




def __plotROC_projMult(newlocation, allsimparams, metaparams):
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



