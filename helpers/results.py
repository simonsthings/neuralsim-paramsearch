import numpy as np
import helpers
#from SimonsPythonHelpers import nestedPrint
import os, pickle

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



def __read_2D_result_data(params, somesimparams, paramdotpathX, paramdotpathY):

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


def fetch_2D_result_data(params, somesimparams, paramdotpathX, paramdotpathY, paramGroupString, useCache=True):
	shortParamStringX = helpers.parameters.getDependentParameterShortNameString(params, paramdotpathX)
	shortParamStringY = helpers.parameters.getDependentParameterShortNameString(params, paramdotpathY)
	
	# if-clause because we cannot be sure that all known results everywhere have metaparams.cache_path defined.
	if 'cache_path' in params.metaparams.keys():
		cachePath = params.metaparams.cache_path
		cacheName = 'cacheFinalAccuracy2D' + '_' + params.metaparams.cache_basename + '_' + shortParamStringX + 'VS' + shortParamStringY + '__' + paramGroupString + '.pickle'
	else:
		cachePath = params.metaparams.figures_path[:-8] + 'cache/'
		cacheName = 'cacheFinalAccuracy2D' + '_' + params.metaparams.datafig_basename + '_' + shortParamStringX + 'VS' + shortParamStringY + '__' + paramGroupString + '.pickle'

	if not os.path.exists(cachePath):
		os.makedirs(cachePath)

	if useCache and os.path.isfile(cachePath + cacheName):
		print "Using cache file '"+cachePath + cacheName+"' instead of re-reading data."
		
		# todo unpickle cached data and return.
		with open(cachePath + cacheName, 'r') as cacheFile:
			results_from_cache = pickle.load(cacheFile)
		return results_from_cache
	
	else:
		if useCache:
			cacheString = "No cache found."
		else:
			cacheString = "No cache reading allowed."
		print cacheString + " Reading data folder and writing to new cache file '" + cachePath + cacheName + "'."
		
		# actually read results from data folder structure (or perhaps some remote, huge, distributed database in the future?)
		new_results = helpers.results.__read_2D_result_data(params, somesimparams, paramdotpathX, paramdotpathY)

		with open(cachePath + cacheName, 'w') as cacheFile:
			pickle.dump(new_results,cacheFile,protocol=2)  # protocol 2 should be a compressed, binary format.
		return new_results


def fetch_3D_result_data_grouped(params, somesimparams, paramdotpathX, paramdotpathY, paramdotpathZ, paramGroupString='', useCache=True):
	
	# split given list of somesimparams into separate list for each entry of paramdotpathZ:
	groupedParamSets = helpers.parameters.splitByParameter(somesimparams, params.flatParamLists, [paramdotpathZ])
	
	threeD_data = {'dim1dim2_datasets':[] , 'dim3_tickvalues':[]}
	for paramSubGroupString in groupedParamSets.keys():
		paramSubgroup = groupedParamSets[paramSubGroupString]
		combinedParamGroupString = helpers.parameters.insertParamStringIntoGroupString(paramGroupString,paramSubGroupString)
		results_2D = fetch_2D_result_data(params,paramSubgroup,paramdotpathX,paramdotpathY,combinedParamGroupString)
		threeD_data['dim1dim2_datasets'].append(results_2D)

		tickvalue = helpers.parameters.getParamRecursively(paramdotpathZ, paramSubgroup[0])
		threeD_data['dim3_tickvalues'].append(tickvalue)

	return threeD_data


def fetch_MultiDim_result_data(params, somesimparams, paramdotpathList, paramGroupString='', useCache=True):
	shortParamStringX = helpers.parameters.getDependentParameterShortNameString(params, paramdotpathList[0])
	shortParamStringY = helpers.parameters.getDependentParameterShortNameString(params, paramdotpathList[1])
	shortParamStringZ = helpers.parameters.getDependentParameterShortNameString(params, paramdotpathList[2])
	
	raise NotImplementedError

