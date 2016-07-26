import numpy as np
import helpers
#from SimonsPythonHelpers import nestedPrint


def read_result_data_1D(metaparams, somesimparams, paramdotpath):
	theTicks = []
	true_positive_rates = np.zeros((len(somesimparams), metaparams.numRepetitions));
	false_positive_rates = np.zeros((len(somesimparams), metaparams.numRepetitions));
	for sid in xrange(len(somesimparams)):
		simparams = somesimparams[sid]
		paramValue = helpers.parameters.getParamRecursively(paramdotpath, simparams)
		theTicks.append(paramValue)

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
	return true_positive_rates, false_positive_rates, theTicks



def read_result_data_2D(params, somesimparams, paramdotpathX, paramdotpathY):

	xTicks = np.array(params.flatParamLists[paramdotpathX])
	yTicks = np.array(params.flatParamLists[paramdotpathY])

	true_positive_rates = np.zeros((len(xTicks), len(yTicks), params.metaparams.numRepetitions));
	false_positive_rates = np.zeros((len(xTicks), len(yTicks), params.metaparams.numRepetitions));

	for sid in xrange(len(somesimparams)):
		simparams = somesimparams[sid]
		paramValueX = helpers.parameters.getParamRecursively(paramdotpathX, simparams)
		paramValueY = helpers.parameters.getParamRecursively(paramdotpathY, simparams)

		xIndex = (xTicks == paramValueX)
		yIndex = (yTicks == paramValueY)

		for repetitionID in xrange(params.metaparams.numRepetitions):
			repfolder = params.metaparams.repetitionFoldernames[repetitionID]
			stimdetfilename = params.metaparams.data_path + simparams.extendedparamFoldername + '/' + repfolder + '/' + params.metaparams.figures_basename + '.stimulusdetectionstatistics.txt'
			simdata = np.genfromtxt(stimdetfilename,
									# names="time,tpr,fpr,t_div_f",
									names="tpr,fpr,t_div_f",
									comments='#',  # skip comment lines
									dtype=None
									)  # guess dtype of each column
			true_positive_rates[xIndex, yIndex, repetitionID] = simdata['tpr'][-1];
			false_positive_rates[xIndex, yIndex, repetitionID] = simdata['fpr'][-1];

	return true_positive_rates, false_positive_rates, xTicks, yTicks

