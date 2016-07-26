import dotmap
import matplotlib.pyplot as plt
from numpy import arange
import numpy as np
import os
import helpers
from SimonsPythonHelpers import nestedPrint


def makeFig(params, paramdotpathX, paramdotpathY):

	figtypename = 'TwoParams2D_Accuracy'

	print "Making figure type " + figtypename + " for parameters '" + paramdotpathY + "' versus '" + paramdotpathX + "'."

	# make a copy of the list:
	otherParamStringsList = list(params.flatParamLists.keys())

	if paramdotpathX in params.flatParamLists.keys():
		otherParamStringsList.remove(paramdotpathX)
	else:
		print "Skipping figure generation because parameter '" + paramdotpathX + "' was not found among the extended params lists."
		return
	if paramdotpathY in params.flatParamLists.keys():
		otherParamStringsList.remove(paramdotpathY)
	else:
		print "Skipping figure generation because parameter '" + paramdotpathY + "' was not found among the extended params lists."
		return


	if otherParamStringsList:  # if there are free parameters that require separate figures to be generated:
		groupedParamSets = helpers.parameters.splitByParameter(params.allsimparams, params.flatParamLists, otherParamStringsList)
		# print "The type of groupedParamSets is "+str(type(groupedParamSets))
		#nestedPrint(groupedParamSets,maxDepth=2)

		# nestedPrint(groupedParamSets,maxDepth=3)

		print "Making figure for parameters '"+paramdotpathX+"' and '"+paramdotpathY+"', but not for other parameters: "+ str(otherParamStringsList)


		# rearrange allsimparams into groups of otherparams with only varying values of paramdotpath:
		# do something for each value of each parameter except the given paramdotpath!
		# get subset of allsimparams where

		for paramGroupString in groupedParamSets.keys():
			paramSubgroup = groupedParamSets[paramGroupString]

			_doThePlotting(params, paramSubgroup, paramGroupString, paramdotpathX, paramdotpathY, figtypename)

	else:  # all parameter sets can be represented in a single figure:
		_doThePlotting(params, params.allsimparams, "theOnlyFigure", paramdotpathX, paramdotpathY, figtypename)


def _doThePlotting(params, somesimparams, paramGroupString, paramdotpathX, paramdotpathY, figtypename):

	metaparams = params.metaparams

	shortParamStringX = helpers.parameters.getDependentParameterShortNameString(params,paramdotpathX)
	shortParamStringY = helpers.parameters.getDependentParameterShortNameString(params,paramdotpathY)

	figBlob = figtypename + '_' + shortParamStringX+'VS'+shortParamStringY
	figPath = metaparams.figures_path + 'figtype_' + figBlob + '/'
	os.system('mkdir -p ' + figPath)

	true_positive_rates, false_positive_rates, xTicks, yTicks = helpers.results.read_result_data_2D(params, somesimparams, paramdotpathX, paramdotpathY)

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

	_plotStuff(axesdims, true_positive_rates, false_positive_rates, xTicks, yTicks, shortParamStringX, shortParamStringY)

	#__plotAccuracies_param1_Repetitions(location1, somesimparams, metaparams, 'tpr', paramdotpath)
	#__plotAccuracies_param1_Repetitions(location2, somesimparams, metaparams, 'fpr', paramdotpath)
	#__plotTPRvsFPR_projMult(location3, somesimparams, metaparams, paramdotpath)
	#__plotROC_projMult(location4, somesimparams, metaparams)

	figName = metaparams.figures_basename + '_' + figBlob + '__' + paramGroupString
	figAccuracies.savefig(figPath + figName + '.png')
	plt.close(figAccuracies)


def _plotStuff(axesdims, true_positive_rates, false_positive_rates, xTicks, yTicks, shortParamStringX, shortParamStringY):

	meanTPRs = true_positive_rates.mean(axis=2)
	meanFPRs = false_positive_rates.mean(axis=2)
	varTPRs = true_positive_rates.var(axis=2)
	varFPRs = false_positive_rates.var(axis=2)

	#sensitivityIndex = (meanTPRs - meanFPRs) / np.sqrt( 0.5 * (varTPRs + varFPRs) ) # from e.g. https://en.wikipedia.org/wiki/Sensitivity_and_specificity
	cheapAccuracy = meanTPRs - meanFPRs

	readableLabelX = shortParamStringX.replace('WITH',' (with ').replace('AND',' and ')
	readableLabelY = shortParamStringY.replace('WITH',' (with ').replace('AND',' and ')
	readableLabelX = readableLabelX+')' if not readableLabelX == shortParamStringX else readableLabelX
	readableLabelY = readableLabelY+')' if not readableLabelY == shortParamStringY else readableLabelY

	location = [axesdims.x1, axesdims.y1, axesdims.w1, axesdims.h1]
	fig = plt.gcf()
	ax = fig.add_axes(location, title='Sensitivity (true positive rate)')
	plt.imshow(meanTPRs.T, aspect='auto', interpolation='nearest')
	plt.xticks(np.r_[0:len(xTicks)], xTicks)
	plt.yticks(np.r_[0:len(yTicks)], yTicks)
	plt.clim(0,1)
	theYlims = plt.ylim()
	plt.ylim([theYlims[1],theYlims[0]])
	plt.xlabel(readableLabelX)
	plt.ylabel(readableLabelY)
	currentXTicks = plt.xticks()
	if len(xTicks) > 10:
		idx = np.r_[1:len(xTicks):round(len(xTicks)/10)].astype(int)
		#print "idx: " + str(idx)
		for id in idx:
			currentXTicks[1][id]._text = ''
	plt.xticks( *currentXTicks)


	location = [axesdims.x2, axesdims.y1, axesdims.w2, axesdims.h1]
	fig = plt.gcf()
	ax = fig.add_axes(location, title='1-Specificity (false positive rate)')
	plt.imshow(meanFPRs.T, aspect='auto', interpolation='nearest')
	plt.xticks(np.r_[0:len(xTicks)], xTicks)
	plt.yticks(np.r_[0:len(yTicks)], yTicks)
	plt.clim(0, 1)
	theYlims = plt.ylim()
	plt.ylim([theYlims[1], theYlims[0]])
	plt.xlabel(readableLabelX)
	plt.ylabel(readableLabelY)
	currentXTicks = plt.xticks()
	if len(xTicks) > 10:
		idx = np.r_[1:len(xTicks):round(len(xTicks)/10)].astype(int)
		#print "idx: " + str(idx)
		for id in idx:
			currentXTicks[1][id]._text = ''
	plt.xticks( *currentXTicks)


	location = [axesdims.x3, axesdims.y1, axesdims.w3, axesdims.h1]
	fig = plt.gcf()
	#ax = fig.add_axes(location, title='"Sensitivity index" ( (tpr-fpr) / sqrt((vartp+varfp)/2) )')
	ax = fig.add_axes(location, title='tpr - fpr')
	plt.imshow(cheapAccuracy.T, aspect='auto', interpolation='nearest')
	plt.xticks(np.r_[0:len(xTicks)], xTicks)
	plt.yticks(np.r_[0:len(yTicks)], yTicks)
	plt.clim(0, 1)
	theYlims = plt.ylim()
	plt.ylim([theYlims[1], theYlims[0]])
	plt.xlabel(readableLabelX)
	plt.ylabel(readableLabelY)
	#plt.colorbar(label='dlas')
	plt.colorbar()
	currentXTicks = plt.xticks()
	if len(xTicks) > 10:
		idx = np.r_[1:len(xTicks):round(len(xTicks)/10)].astype(int)
		#print "idx: " + str(idx)
		for id in idx:
			currentXTicks[1][id]._text = ''
	plt.xticks( *currentXTicks)


	pass















