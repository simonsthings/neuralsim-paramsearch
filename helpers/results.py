import numpy as np
import helpers
#from SimonsPythonHelpers import nestedPrint


#def read_1D_Accuracy(metaparams, somesimparams, paramdotpath):
#	(theTicks, true_positive_rates, false_positive_rates, sufficientSelectivitySpecificityOnsets) = read_1D_result_data(metaparams, somesimparams, paramdotpath, None)
#	return true_positive_rates, false_positive_rates, theTicks


#def read_1D_SelectivityOnsetTime(metaparams, somesimparams, paramdotpath, requestedMinimumDistance=0.75):
#	(theTicks, true_positive_rates, false_positive_rates, sufficientSelectivitySpecificityOnsets) = read_1D_result_data(metaparams, somesimparams, paramdotpath, requestedMinimumDistance)
#	return theTicks, sufficientSelectivitySpecificityOnsets


def read_1D_result_data(metaparams, somesimparams, paramdotpath, requestedMinimumDistance=0.75):
	theTicks = []
	true_positive_rates = np.zeros((len(somesimparams), metaparams.numRepetitions))
	false_positive_rates = np.zeros((len(somesimparams), metaparams.numRepetitions))
	sufficientSelectivitySpecificityOnsets = np.zeros((len(somesimparams), metaparams.numRepetitions))
	firstGoodRows = np.zeros((len(somesimparams), metaparams.numRepetitions))

	for sid in xrange(len(somesimparams)):
		simparams = somesimparams[sid]
		paramValue = helpers.parameters.getParamRecursively(paramdotpath, simparams)
		theTicks.append(paramValue)

		for repetitionID in xrange(metaparams.numRepetitions):
			repfolder = metaparams.repetitionFoldernames[repetitionID]
			stimdetfilename = metaparams.data_path + simparams.extendedparamFoldername + '/' + repfolder + '/' + metaparams.figures_basename + '.stimulusdetectionstatistics.txt'
			simdata = np.genfromtxt(stimdetfilename,
									# names="time,tpr,fpr,t_div_f",
									names="time,tpr,fpr,tprMinusfpr,tprDivfpr",
									comments='#',  # skip comment lines
									dtype=None
									)  # guess dtype of each column
			
			if requestedMinimumDistance:
				firstGoodRow = -1
				for row in xrange(len(simdata['time'])-1,-1,-1):
					if (simdata['tprMinusfpr'][row]) >= requestedMinimumDistance :
						firstGoodRow = row
				
				if firstGoodRow >= 0:
					thetime = simdata['time'][firstGoodRow]
				else:
					thetime=np.nan
				sufficientSelectivitySpecificityOnsets[sid, repetitionID] = thetime
				firstGoodRows[sid, repetitionID] = firstGoodRow

			true_positive_rates[sid, repetitionID] = simdata['tpr'][-1]
			false_positive_rates[sid, repetitionID] = simdata['fpr'][-1]
			
	#print firstGoodRows
	#print sufficientSelectivitySpecificityOnsets

	return theTicks, true_positive_rates, false_positive_rates, sufficientSelectivitySpecificityOnsets



def read_2D_result_data(params, somesimparams, paramdotpathX, paramdotpathY):

	xTicks = np.array(params.flatParamLists[paramdotpathX])
	yTicks = np.array(params.flatParamLists[paramdotpathY])

	true_positive_rates = np.zeros((len(xTicks), len(yTicks), params.metaparams.numRepetitions))
	false_positive_rates = np.zeros((len(xTicks), len(yTicks), params.metaparams.numRepetitions))

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
									names="time,tpr,fpr,tprMinusfpr,tprDivfpr",
									comments='#',  # skip comment lines
									dtype=None
									)  # guess dtype of each column
			true_positive_rates[xIndex, yIndex, repetitionID] = simdata['tpr'][-1]
			false_positive_rates[xIndex, yIndex, repetitionID] = simdata['fpr'][-1]

	return true_positive_rates, false_positive_rates, xTicks, yTicks

