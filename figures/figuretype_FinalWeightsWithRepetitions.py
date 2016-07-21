import os

import matplotlib.pyplot as plt
import numpy as np
from dotmap import DotMap


def makeFigs(params, paramFullPath=None):

	figtypename = 'FinalWeightsWithRepetitions'

	print "Making figure type "+figtypename+" for all parameters."

	allsimparams = params.allsimparams
	metaparams = params.metaparams
	paramGroupString = "theOnlyFigureHere" # could come from helpers.parameters.splitByParameter(..) in the future.

	axesdims = DotMap()
	axesdims.figFinalWeights.x1 = 0.1
	axesdims.figFinalWeights.w1 = 0.8
	axesdims.figFinalWeights.y1 = 0.05
	axesdims.figFinalWeights.h1 = 0.9

	for simparams in allsimparams:
		print "Drawing "+figtypename+" figure for simulations that have '"+ simparams.extendedparamFoldername[5:] + "' in common."
		figFinalWeights = plt.figure(figsize=(6, 12))
		__plotFinalWeights(axesdims, simparams, metaparams)

		(figPath, figName) = __prepareFigurePathAndName(simparams, metaparams, paramGroupString, paramFullPath, figtypename)
		figFinalWeights.savefig(figPath + figName + '.png')
		plt.close(figFinalWeights)

		# save this figure's path for later reference during html file generation:
		simparams.figures[figtypename] = figPath[len(metaparams.figures_path):] + figName

	__make_html(allsimparams, metaparams, figtypename)


def __make_html(allsimparams, metaparams, figtypename):
	htmlfile = open(metaparams.figures_path + '/overview_'+figtypename+'.html', 'w')

	htmlfile.write('<html> \n')
	htmlfile.write('<body> \n')
	htmlfile.write('<table><tr> \n')

	for simparams in allsimparams:
		imglink = simparams.figures[figtypename] + '.png'
		htmlfile.write('<td><img src=' + imglink + ' /></td>')

	htmlfile.write('</tr></table> \n')
	htmlfile.write('</body> \n')
	htmlfile.write('</html> \n')
	htmlfile.close()


def __prepareFigurePathAndName(simparams, metaparams, paramGroupString, paramFullPath, figtypename):

	if not paramFullPath:
		shortParamString = 'allparams'
	else:
		shortPrarmStringID = paramFullPath.rfind('.')
		shortParamString = paramFullPath[shortPrarmStringID + 1:]
		print "WARNING: parameter-spefificity not yet implemented for this figure type!"

	figBlob = figtypename+'_' + shortParamString + ''
	figPath = metaparams.figures_path + 'figtype_' + figBlob + '/' + simparams.extendedparamFoldername + '/'
	figName = metaparams.figures_basename + '_' + figBlob + '__' + paramGroupString
	os.system('mkdir -p ' + figPath)

	return figPath,figName


def __plotFinalWeights(axesdims, simparams, metaparams):
	newlocation = [axesdims.figFinalWeights.x1, axesdims.figFinalWeights.y1, axesdims.figFinalWeights.w1,
				   axesdims.figFinalWeights.h1]
	fig = plt.gcf()
	ax = fig.add_axes(newlocation, title='final weights (' + str(metaparams.numRepetitions) + ' repetitions)')

	finalweights = __readFinalWeights(simparams, metaparams)

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


def __readFinalWeights(simparams, metaparams):
	finalweights = np.zeros([metaparams.numRepetitions, simparams.neurongroups.inputs.N])

	for repetitionID in xrange(metaparams.numRepetitions):
		repfolder = metaparams.repetitionFoldernames[repetitionID]
		#os.system('mkdir -p ' + metaparams.figures_path + simparams.extendedparamFoldername)

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
