import dotmap
import matplotlib.pyplot as plt
from numpy import arange
import numpy as np
import os
import helpers
#from SimonsPythonHelpers import nestedPrint


def makeFig(params, paramdotpathX, paramdotpathY, strideValueToShow=None):

	# extracting future figure file name from script file name:
	scriptfilename = os.path.basename(__file__)
	figtypename = scriptfilename[len('figuretype_'):scriptfilename.rfind('.py')] # may end on either .py or .pyc
	print "Making figure type " + figtypename + " for parameters '" + paramdotpathY + "' and '"+paramdotpathY+"', with each 'stride' value."

	# make a copy of the list:
	stillWithStrideParamStringsList = list(params.flatParamLists.keys())

	if paramdotpathX in params.flatParamLists.keys():
		stillWithStrideParamStringsList.remove(paramdotpathX)
	else:
		print "Skipping figure generation because parameter '" + paramdotpathX + "' was not found among the extended params lists."
		return
	if paramdotpathY in params.flatParamLists.keys():
		stillWithStrideParamStringsList.remove(paramdotpathY)
	else:
		print "Skipping figure generation because parameter '" + paramdotpathY + "' was not found among the extended params lists."
		return
	
	paramdotpathStride = None
	for flatparam in params.flatParamLists.keys():
		if ".driftcompensation.stride" in flatparam:
			paramdotpathStride = flatparam
	if not paramdotpathStride:
		print "Skipping figure generation because parameter name containing '.driftcompensation.stride' was not found among the extended params lists."
		return
	
	# remove also the third ('stride') param:
	otherParamStringsList = list(stillWithStrideParamStringsList)
	otherParamStringsList.remove(paramdotpathStride)


	if otherParamStringsList:  # if there are free parameters that require separate figures to be generated:
		groupedParamSets = helpers.parameters.splitByParameter(params.allsimparams, params.flatParamLists, otherParamStringsList)
		# print "The type of groupedParamSets is "+str(type(groupedParamSets))
		#nestedPrint(groupedParamSets,maxDepth=2)

		# nestedPrint(groupedParamSets,maxDepth=3)

		print "- generating a figure for parameters '"+paramdotpathX+"' and '"+paramdotpathY+"', for each of '"+paramdotpathStride+"', but not for other parameters: "+ str(otherParamStringsList)

		# rearrange allsimparams into groups of otherparams with only varying values of paramdotpath:
		# do something for each value of each parameter except the given paramdotpath!
		# get subset of allsimparams where

		for paramGroupString in groupedParamSets.keys():
			paramSubgroup = groupedParamSets[paramGroupString]

			_doThePlotting(params, paramSubgroup, paramGroupString, paramdotpathX, paramdotpathY, paramdotpathStride, figtypename)

	else:  # all parameter sets can be represented in a single figure:
		print "- generating one figure for parameters '" + paramdotpathX + "' and '" + paramdotpathY + "', for each of '" + paramdotpathStride + "'."
		_doThePlotting(params, params.allsimparams, "", paramdotpathX, paramdotpathY, paramdotpathStride, figtypename)


def _doThePlotting(params, somesimparams, paramGroupString, paramdotpathX, paramdotpathY, paramdotpathZ, figtypename):

	metaparams = params.metaparams
	
	shortParamStringX = helpers.parameters.getDependentParameterShortNameString(params, paramdotpathX)
	shortParamStringY = helpers.parameters.getDependentParameterShortNameString(params, paramdotpathY)
	
	figBlob = figtypename + '_' + shortParamStringX+'VS'+shortParamStringY
	figPath = metaparams.figures_path + 'figtype_' + figBlob + '/'
	os.system('mkdir -p ' + figPath)

	#threeD_data = helpers.results.fetch_2D_result_data(params, somesimparams, paramdotpathX, paramdotpathY,paramGroupString)
	threeD_data = helpers.results.fetch_3D_result_data_grouped(params, somesimparams, paramdotpathX, paramdotpathY, paramdotpathZ, paramGroupString)

	fs = (20 ,6)
	axesdims = dotmap.DotMap()
	axesdims.x1 = 0.05
	axesdims.x2 = 0.35
	axesdims.x3 = 0.65
	axesdims.w1 = 0.25
	axesdims.w2 = 0.25
	axesdims.w3 = 0.3

	axesdims.y1 = 0.1
	axesdims.h1 = 0.8

	figAccuracies = plt.figure(figsize=fs)

	readableParamStringX = helpers.parameters.getReadableParamString(params, paramdotpathX)
	readableParamStringY = helpers.parameters.getReadableParamString(params, paramdotpathY)
	readableParamStringZ = helpers.parameters.getReadableParamString(params, paramdotpathZ)

	_plotStuff(axesdims, threeD_data, readableParamStringX, readableParamStringY, readableParamStringZ)

	#__plotAccuracies_param1_Repetitions(location1, somesimparams, metaparams, 'tpr', paramdotpath)
	#__plotAccuracies_param1_Repetitions(location2, somesimparams, metaparams, 'fpr', paramdotpath)
	#__plotTPRvsFPR_projMult(location3, somesimparams, metaparams, paramdotpath)
	#__plotROC_projMult(location4, somesimparams, metaparams)
	
	figAccuracies.text(0.05,0.97,paramGroupString)
	
	if paramGroupString:
		figName = metaparams.figures_basename + '_' + figBlob + '__' + paramGroupString
	else:
		figName = metaparams.figures_basename + '_' + figBlob + '__theOnlyFigure'
	figAccuracies.savefig(figPath + figName + '.png')
	plt.close(figAccuracies)


def _plotStuff(axesdims, threeD_data, readableLabelX, readableLabelY, readableParamStringZ):
	
	tpr_zerothStride, fpr_zerothStride, xTicks, yTicks = threeD_data['dim1dim2_datasets'][0]
	meanTPRs_zerothStride = tpr_zerothStride.mean(axis=2)
	meanFPRs_zerothStride = fpr_zerothStride.mean(axis=2)
	#varTPRs = tpr_zerothStride.var(axis=2)
	#varFPRs = fpr_zerothStride.var(axis=2)
	#sensitivityIndex = (meanTPRs - meanFPRs) / np.sqrt( 0.5 * (varTPRs + varFPRs) ) # from e.g. https://en.wikipedia.org/wiki/Sensitivity_and_specificity
	cheapAccuracy_zerothStride = meanTPRs_zerothStride - meanFPRs_zerothStride
	cheapAccuracy_zerothStride[cheapAccuracy_zerothStride < 0] = 0    # accuracy doesn't make sense to be negative.
	sum_cheapAccuracy_zerothStride = np.sum(cheapAccuracy_zerothStride)


	# compute the relative improvements versus zeroth stride value (= likely "no growth")
	allstrides = threeD_data['dim3_tickvalues']
	sums_cheapAccuracy = []
	ratios_cheapAccuracy = []
	diffs_cheapAccuracy = []
	maxImprovement_diffs = -99999 # whatevs
	maxImprovement_id = 0
	maxImprovement_cheapAccuracy = cheapAccuracy_zerothStride  # init before loop
	for sid in xrange(len(allstrides)):
		
		true_positive_rates, false_positive_rates, xTicks, yTicks = threeD_data['dim1dim2_datasets'][sid]
		
		meanTPRs = true_positive_rates.mean(axis=2)
		meanFPRs = false_positive_rates.mean(axis=2)
		varTPRs = true_positive_rates.var(axis=2)
		varFPRs = false_positive_rates.var(axis=2)
		
		# sensitivityIndex = (meanTPRs - meanFPRs) / np.sqrt( 0.5 * (varTPRs + varFPRs) ) # from e.g. https://en.wikipedia.org/wiki/Sensitivity_and_specificity
		cheapAccuracy = meanTPRs - meanFPRs
		cheapAccuracy[cheapAccuracy < 0] = 0   # accuracy doesn't make sense to be negative.
		sums_cheapAccuracy.append(np.sum(cheapAccuracy))
		ratios_cheapAccuracy.append(sum_cheapAccuracy_zerothStride / sums_cheapAccuracy[-1])
		diffs_cheapAccuracy.append( sums_cheapAccuracy[-1] - sum_cheapAccuracy_zerothStride)

		if diffs_cheapAccuracy[-1] > maxImprovement_diffs:
			maxImprovement_id = sid
			maxImprovement_cheapAccuracy = cheapAccuracy
			maxImprovement_diffs = diffs_cheapAccuracy[-1]
		pass
		

	location = [axesdims.x1, axesdims.y1, axesdims.w1, axesdims.h1]
	fig = plt.gcf()
	#ax = fig.add_axes(location, title='"Sensitivity index" ( (tpr-fpr) / sqrt((vartp+varfp)/2) )')
	ax = fig.add_axes(location, title='tpr - fpr (0th '+readableParamStringZ+' val: likely No growth)')
	plt.imshow(cheapAccuracy_zerothStride.T, aspect='auto', interpolation='nearest')
	xTickIDs = np.int32(np.round(np.linspace( 0 , len(xTicks)-1 , 5)))
	yTickIDs = np.int32(np.round(np.linspace( 0 , len(yTicks)-1 , 5)))
	plt.xticks(xTickIDs, xTicks[[xTickIDs]])
	plt.yticks(yTickIDs, yTicks[[yTickIDs]])
	plt.clim(0, 1)
	theYlims = plt.ylim()
	plt.ylim([theYlims[1], theYlims[0]])
	plt.xlabel(readableLabelX)
	plt.ylabel(readableLabelY)
	#plt.colorbar(label='dlas')
	plt.colorbar()


	location = [axesdims.x2, axesdims.y1, axesdims.w2, axesdims.h1]
	fig = plt.gcf()
	#ax = fig.add_axes(location, title='"Sensitivity index" ( (tpr-fpr) / sqrt((vartp+varfp)/2) )')
	ax = fig.add_axes(location, title='tpr - fpr (best '+readableParamStringZ+' val: With growth)')
	plt.imshow(maxImprovement_cheapAccuracy.T, aspect='auto', interpolation='nearest')
	xTickIDs = np.int32(np.round(np.linspace( 0 , len(xTicks)-1 , 5)))
	yTickIDs = np.int32(np.round(np.linspace( 0 , len(yTicks)-1 , 5)))
	plt.xticks(xTickIDs, xTicks[[xTickIDs]])
	plt.yticks(yTickIDs, yTicks[[yTickIDs]])
	plt.clim(0, 1)
	theYlims = plt.ylim()
	plt.ylim([theYlims[1], theYlims[0]])
	plt.xlabel(readableLabelX)
	plt.ylabel(readableLabelY)
	#plt.colorbar(label='dlas')
	plt.colorbar()


	location = [axesdims.x3, axesdims.y1, axesdims.w3, axesdims.h1]
	fig = plt.gcf()
	#ax = fig.add_axes(location, title='"Sensitivity index" ( (tpr-fpr) / sqrt((vartp+varfp)/2) )')
	ax = fig.add_axes(location, title='improvement for all '+readableParamStringZ+' values')
	plt.plot(allstrides, diffs_cheapAccuracy, label='4th param X',linewidth=2.0)
	plt.legend()
	pass















