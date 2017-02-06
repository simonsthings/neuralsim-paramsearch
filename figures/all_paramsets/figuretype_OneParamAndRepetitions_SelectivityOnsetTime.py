import numpy as np
import dotmap
import matplotlib.pyplot as plt
from numpy import arange
import os
import helpers
#from SimonsPythonHelpers import nestedPrint


def makeFig(params, paramdotpath, requestedMinimumDistance = 0.75):
	
	# extracting future figure file name from script file name:
	scriptfilename = os.path.basename(__file__)
	figtypename = scriptfilename[len('figuretype_'):scriptfilename.rfind('.py')] # may end on either .py or .pyc
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
				somesimparams = groupedParamSets[paramGroupString]

				__doThePlotting(params, somesimparams, paramGroupString, paramdotpath,figtypename,requestedMinimumDistance)

		else: # all parameter sets can be represented in a single figure:
			__doThePlotting(params, params.allsimparams, "", paramdotpath,figtypename,requestedMinimumDistance)
	else:
		print "Skipping figure generation for param '" + paramdotpath + "' because this parameter was not found among the extended params lists."


def __doThePlotting(params, somesimparams, paramGroupString, paramFullPath, figtypename, requestedMinimumDistance):
	metaparams = params.metaparams

	shortParamString = helpers.parameters.getDependentParameterShortNameString(params, paramFullPath)

	figBlob = figtypename + '_' + shortParamString
	figPath = metaparams.figures_path + 'figtype_' + figBlob + '/'
	if not os.path.exists(figPath):
		os.makedirs(figPath)

	# axesdims = dotmap.DotMap()
	fs = (12, 8)
	# location1 = [0.1 ,0.45 ,0.28 ,0.45]
	# location2 = [0.55 ,0.45 ,0.28 ,0.45]
	location1  = [0.1, 0.75, 0.65, 0.2]
	location1b = [0.78, 0.75, 0.05 / fs[0] * fs[1], 0.2]
	location2  = [0.1, 0.09, 0.65, 0.2]
	location3  = [0.1, 0.42, 0.65, 0.2]
	location4  = [0.85, 0.42, 0.2 / fs[0] * fs[1], 0.2]

	figAccuracies = plt.figure(figsize=fs)
	
	theTicks, true_positive_rates, false_positive_rates, sufficientSelectivitySpecificityOnsets = helpers.results.read_1D_result_data(metaparams, somesimparams, paramFullPath,requestedMinimumDistance)
	readableParamString = helpers.parameters.getReadableParamString(params, paramFullPath)
	
	#nestedPrint(params.baseParams.general)
	#__plotResults_param1_Repetitions(location1, readableParamString, metaparams.numRepetitions, 'true positive rate', true_positive_rates, theTicks)
	__plotResults_selectivityOnset_Repetitions(location1,location1b, readableParamString, metaparams.numRepetitions, 'learning onset times for tpr-fpr >= '+str(requestedMinimumDistance)+'', sufficientSelectivitySpecificityOnsets, theTicks, params.baseParams.general.simtime)
	__plotFirstOnsetTimes(location3, sufficientSelectivitySpecificityOnsets, theTicks, readableParamString, requestedMinimumDistance, params.baseParams.general.simtime)
	#__plotROC_projMult(location4, true_positive_rates, false_positive_rates, theTicks, paramFullPath)

	if paramGroupString:
		figName = metaparams.figures_basename + '_' + figBlob + '__' + paramGroupString + '__requestedDist='+str(requestedMinimumDistance)
	else:
		figName = metaparams.figures_basename + '_' + figBlob + '__theOnlyParams' + '__requestedDist='+str(requestedMinimumDistance)

	figAccuracies.savefig(figPath + figName + '.png')
	plt.close(figAccuracies)


def __plotResults_selectivityOnset_Repetitions(newlocation,locationColorbar, readableParamString, numRepetitions, tprfprString, tpfp_rates, x_ticklabels, simtime):
	fig = plt.gcf()
	cax = fig.add_axes(locationColorbar)
	ax = fig.add_axes(newlocation, title='' + tprfprString + '')
	
	plt.imshow(tpfp_rates.T, aspect='auto', interpolation='nearest')
	
	plt.colorbar(cax=cax, label='onset time (s)')
	plt.clim(0,simtime)
	
	theYticks = arange(numRepetitions)
	plt.yticks(theYticks, theYticks + 1)
	
	plt.ylabel('repetitions')
	plt.xlabel(readableParamString)
	plt.xticks(np.r_[0:len(x_ticklabels)], x_ticklabels)
	
	# not the prettiest of workarounds, but whatever:
	currentXTicks = plt.xticks()
	if len(x_ticklabels) > 10:
		idx = np.r_[1:len(x_ticklabels):round(len(x_ticklabels) / 10)].astype(int)
		# print "idx: " + str(idx)
		for id in idx:
			currentXTicks[1][id]._text = ''
	plt.xticks(*currentXTicks)
	
	# now show the means:
	
	# meanlocation = list(newlocation)
	# meanlocation[0] = newlocation[0] + newlocation[2] + 0.02
	# meanlocation[2] = newlocation[2] / metaparams.numRepetitions
	# ax2 = fig.add_axes(meanlocation, title='mean')
	
	# meanSomethingRates = true_positive_rates.mean(axis=1)
	# plt.imshow(np.expand_dims(meanSomethingRates, axis=1), aspect='auto')
	# plt.xticks([])
	# plt.yticks([])
	pass



def __plotFirstOnsetTimes(newlocation, sufficientSelectivitySpecificityOnsets, x_ticklabels, readableParamString, requestedMinimumDistance, simtime):
	from helpers.parameters import getParamRecursively

	fig = plt.gcf()
	lastax = plt.gca()
	ax = fig.add_axes(newlocation, title='time of first successful learning (for tpr-fpr >= '+str(requestedMinimumDistance)+')')
	
	with np.warnings.catch_warnings():  # suppress warnings temporarily:
		np.warnings.simplefilter("ignore")
		meanTPRs = np.nanmean(sufficientSelectivitySpecificityOnsets, axis=1)
		
		stdTPRs = np.nanstd(sufficientSelectivitySpecificityOnsets, axis=1)
		
	#print 'meanTPRs: '+ str(meanTPRs)
	#print 'stdTPRs: '+ str(stdTPRs)

	# find useful min and max limits for the X axis:
	xmin = x_ticklabels[0] - (x_ticklabels[1]-x_ticklabels[0])/2.0
	xmax = x_ticklabels[-1] + (x_ticklabels[-1]-x_ticklabels[-2])/2.0

	plt.fill_between(x_ticklabels, meanTPRs+stdTPRs, meanTPRs-stdTPRs, color=(1,0.65,0,0.2),linewidth=0.0)

	plt.plot(x_ticklabels, meanTPRs, label='first time at which tpr - fpr >= '+str(requestedMinimumDistance),color=(1,0.65,0),linewidth=2.0)
	#plt.plot(x_ticklabels, meanTPRs, label='first time at which tpr - fpr >= '+str(requestedMinimumDistance),color=(1,0.65,0),linewidth=2.0,marker='o')
	plt.ylim([0, simtime])
	plt.xlim([xmin,xmax])
	plt.xlabel(readableParamString)
	plt.ylabel('time of first successful learning (s)')
	plt.legend(fontsize=8, loc='center left')

	if len(x_ticklabels) > 10:
		idx = np.r_[0:len(x_ticklabels):round(len(x_ticklabels)/10)]
		#print "idx: " + str(idx)
		x_ticklabels = np.array(x_ticklabels)[idx.astype(int)]
	plt.xticks( x_ticklabels)


def __plotROC_projMult(newlocation, true_positive_rates, false_positive_rates, y_label, paramPathString):
	fig = plt.gcf()
	ax = fig.add_axes(newlocation, title='ROC')

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


