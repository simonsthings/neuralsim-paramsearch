import numpy as np
from dotmap import DotMap
import os, sys
import matplotlib.pyplot as plt
from numpy import int32, arange
import peakutils

#from SimonsPythonHelpers import nestedPrint


def _extendParamSet_old(metaparams, baseParams, extendedParams, allsimparams, originalBaseParams=None,
						originalExtendedParams=None, subnodepath=''):
	if originalBaseParams == None:
		originalBaseParams = baseParams
		originalExtendedParams = extendedParams
		subnodepath = ''  # first call
	else:
		subnodepath += '.'

	for nodestring in extendedParams:
		print nodestring

		if nodestring not in baseParams:
			print "Node '" + nodestring + "' was not found in baseParams! Exiting... "
			raise ValueError("(Sub)Node names do not match between baseParams and extendedParams!")
		else:
			print "Ok, a node '" + nodestring + "' of extendedParams was found in baseParams. Continuing."
			theExtendedSubNodeObject = extendedParams[nodestring]
			theBaseSubNodeObject = baseParams[nodestring]
			print type(theBaseSubNodeObject)
			# nestedPrint(theBaseSubNodeObject)

			if type(theBaseSubNodeObject) is DotMap:
				print "Aha it is actually a DotMap itself! So go down one iteration here!"
				_extendParamSet_old(metaparams, theBaseSubNodeObject, theExtendedSubNodeObject, allsimparams,
									originalBaseParams, originalExtendedParams, subnodepath + nodestring)
			else:
				print "The baseParams node here seems to be actual data. Dealing with that now!"
				for datachunk in theExtendedSubNodeObject:
					# print "Copy the whole originalBaseParams and set the given node at path '"+subnodepath+"' to '"+str(datachunk)+"' !"
					baseParams[nodestring] = datachunk  # reference to originalBaseParams !!
					newParams = DotMap(originalBaseParams.toDict())
					newParams.extendedparams[nodestring] = datachunk
					# newParams.extendedparams['other'] = 95
					# newParams[subnodepath+nodestring] = datachunk
					# print "A copy of baseParams was made and "
					# print " baseParams["+subnodepath+nodestring+"]="+str(originalBaseParams[subnodepath+nodestring])+" is now "
					# print "  newParams["+subnodepath+nodestring+"]="+str(newParams[subnodepath+nodestring])
					allsimparams.append(newParams)

	pass  # end of function.


def flattenExtendedParamsets(metaparams, baseParams, extendedParams, originalBaseParams=None,
							 originalExtendedParams=None, subnodepath=''):
	"""
	This doesn't just flatten the given extendedParams DotMap, but also checks if all its nodes actually exist in the given baseParams.
	:param metaparams:
	:param baseParams:
	:param extendedParams:
	:param allsimparams:
	:param originalBaseParams:
	:param originalExtendedParams:
	:param subnodepath:
	:return:
	"""
	if originalBaseParams == None:
		originalBaseParams = baseParams
		originalExtendedParams = extendedParams
		subnodepath = ''  # first call
	else:
		subnodepath += '.'

	stringIndexedParamsLists = {}
	for nodestring in extendedParams:
		# print nodestring

		if nodestring not in baseParams:
			print "Node '" + nodestring + "' was not found in baseParams! Exiting... "
			raise ValueError("(Sub)Node names do not match between baseParams and extendedParams!")
		else:
			# print "Ok, a node '" + nodestring + "' of extendedParams was found in baseParams. Continuing."
			theExtendedSubNodeObject = extendedParams[nodestring]
			theBaseSubNodeObject = baseParams[nodestring]
			# print type(theBaseSubNodeObject)
			# nestedPrint(theBaseSubNodeObject)

			if type(theBaseSubNodeObject) is DotMap:
				# print "Aha it is actually a DotMap itself! So go down one recursion level here!"
				moreParamLists = flattenExtendedParamsets(metaparams, theBaseSubNodeObject, theExtendedSubNodeObject,
														  originalBaseParams, originalExtendedParams, subnodepath + nodestring)
				stringIndexedParamsLists.update(moreParamLists)
			else:
				# print "The baseParams node here seems to be actual data. Dealing with that now!"
				stringIndexedParamsLists[subnodepath + nodestring] = theExtendedSubNodeObject

	return stringIndexedParamsLists


def crossAllParamsets(baseParams, flattenedExtendedParams, allsimparams = []):
	# if dict is empty
	if not flattenedExtendedParams:
		return [baseParams]
	else:
		allLongPathStrings = sorted(flattenedExtendedParams.keys())
		onePath = allLongPathStrings[0]
		oneList = flattenedExtendedParams.pop(onePath)
		
		# so that all numbers in a list produce strings with the same number of charactors!
		formatString = get_formatting_string(oneList)
		
		# recursion! Do the same as below for the remaining params first:
		partialSimParams = crossAllParamsets(baseParams, flattenedExtendedParams ,[])

		for paramvalue in oneList:
			# change the given paramset at the given path
			for simparams in partialSimParams:
				setParamRecursively(onePath, paramvalue, simparams)

				# make a proper(?) copy of simparams struct and append it to allsimparams:
				newParams = DotMap(simparams.toDict())
				newParams.extendedparams[onePath] = formatString.format(paramvalue)
				# print "A copy of baseParams was made and "
				# print " baseParams["+subnodepath+nodestring+"]="+str(originalBaseParams[subnodepath+nodestring])+" is now "
				# print "  newParams["+subnodepath+nodestring+"]="+str(newParams[subnodepath+nodestring])
				allsimparams.append(newParams)

		# print "Length of allsimparams before returning: " + str(len(allsimparams))
		return allsimparams

def get_formatting_string(oneList):
	#return _get_formatting_string_new(oneList)
	return _get_formatting_string_old(oneList)

def _get_formatting_string_new(oneList):
	# get minimum precision (if oneList consists of numbers)!
	# Usage: formatString.format(variable)
	if isinstance(oneList[0], (str, unicode, bool)):
		formatString = '{:}'
	else:
		# first part:
		precList = np.abs(np.asarray(oneList))
		precList = precList[precList != 0]
		beforeDot = int(np.log10(np.max(precList)))+1
		
		# second part:
		afterDot = 0
		import decimal   # only used here. Therefore don't import at top of this module.
		for val in oneList:
			d = decimal.Decimal(str(val))
			afterDot = np.min([ d.as_tuple().exponent , afterDot])

		formatString = '{:' + str(beforeDot) + '.' + str(-afterDot) + 'f}'
	return formatString

# maybe still needed to read old cache files (Before February 2017):
def _get_formatting_string_old(oneList):
	# get minimum precision (if oneList consists of numbers)!
	# Usage: formatString.format(variable)
	if isinstance(oneList[0], (str, unicode)):
		formatString = '{:s}'
	else:
		precList = np.abs(np.asarray(oneList))
		precList = precList[precList != 0]
		minvalprecision = int(np.floor(np.min(np.log10(precList))))
		formatString = '{:.' + str(-minvalprecision) + 'f}'
	return formatString


def asStringList(oneList):
	formatString = get_formatting_string(oneList)
	outputList = []
	
	for oneParamValue in oneList:
		outputList.append(formatString.format(oneParamValue))
	return outputList


def splitByParameter(allsimparams,flattenedExtendedParams,paramStringsList):
	"""
	This function groups parameter sets for each figure. Each new figure will be referenced by a new dict entry,
	where the key is a string of the figure name (which also contains any fixed parameter values per figure),
	and as value the dict contains a list of parameter sets that should be used to construct each figure.
	"""
	if not paramStringsList:
		return allsimparams  # or whatever
	else:

		#remainingParamStringsList = paramStringsList
		#oneParamString = remainingParamStringsList.pop()


		oneParamString = paramStringsList[0]
		remainingParamStringsList = list(paramStringsList)
		remainingParamStringsList.remove(oneParamString)

		#shortPrarmStringID = oneParamString.rfind('.')
		#shortParamString = oneParamString[shortPrarmStringID + 1:]

		perValueSimparams = {}

		#print "The param fullpath string: " + oneParamString
		#print "All values of this param: " + str(flattenedExtendedParams[oneParamString])

		formatString = get_formatting_string(flattenedExtendedParams[oneParamString])
		for oneParamValue in flattenedExtendedParams[oneParamString]:
			#print "The Value: "+str(oneParamValue)

			newsimparamsList = []
			for simparams in allsimparams:
				#if simparams.extendedparams[oneParamString] == oneParamValue:
				if getParamRecursively(oneParamString,simparams) == oneParamValue:
					newsimparamsList.append(simparams)
					#allsimparams.remove(simparams)

			subdict = splitByParameter(newsimparamsList,flattenedExtendedParams,remainingParamStringsList)
			#thisPartialKey = shortParamString+str(oneParamValue)
			thisPartialKey = oneParamString+'='+formatString.format(oneParamValue)
			#print "type(subdict): " + str(type(subdict))
			if type(subdict) is list:
				perValueSimparams[thisPartialKey] = subdict
			else: # assume dict
				for subkey in subdict.keys(): # flatten subdict into this dict
					perValueSimparams[thisPartialKey+'_'+subkey] = subdict[subkey]

		return perValueSimparams



def setParamRecursively(onePath, paramvalue, simparams):
	# change the given param at the given path
	if '.' in onePath:
		firstDotPos = onePath.find('.')
		firstNodeString = onePath[:firstDotPos]
		otherNodesString = onePath[ firstDotPos +1:]
		setParamRecursively(otherNodesString, paramvalue, simparams[firstNodeString])
	else:
		simparams[onePath] = paramvalue
		# print "Changed simparam value of node "+onePath+" to " + str(paramvalue)


def getParamRecursively(onePath, simparams):
	# change the given param at the given path
	if '.' in onePath:
		firstDotPos = onePath.find('.')
		firstNodeString = onePath[:firstDotPos]
		otherNodesString = onePath[ firstDotPos +1:]
		return getParamRecursively(otherNodesString, simparams[firstNodeString])
	else:
		return simparams[onePath]




def adjustDependentParameters(params):
	"""
	Goes through each of the previously generated simparams, and adjusts some dependent parameters based on a combination of others.
	:param params:
	:return:
	"""

	# do the following for each defined dependent param:
	for targetParamString in params.dependentParams.keys():

		# compute new dependent param value for each simparams set:
		for simparams in params.allsimparams:

			# start with the baseParam value and scale it by the dependent values:
			newvalue = getParamRecursively(targetParamString, params.baseParams.toDict())
			#print "old value of '"+targetParamString+"': " + str(newvalue)

			#nestedPrint(params.baseParams)
			#print "simparams.connectionsets.con1.maximumweight: " + str(simparams.connectionsets.con1.maximumweight)
			#print "simparams.connectionsets.con1.stdprule.learningrate: " + str(simparams.connectionsets.con1.stdprule.learningrate)

			# compute the new value and apply:
			for operationTuple in params.dependentParams[targetParamString]:

				(applyOp , sourceParamString , scaleOp , scaleValue) = operationTuple

				sourceparamValue = getParamRecursively(sourceParamString, simparams.toDict())
				#print "Source param '"+sourceParamString+"' is: "+str(sourceparamValue)

				if   scaleOp == '*':
					modifiedSourceparamValue = sourceparamValue * scaleValue
				elif scaleOp == '/':
					modifiedSourceparamValue = sourceparamValue / scaleValue
				elif scaleOp == '+':
					modifiedSourceparamValue = sourceparamValue + scaleValue
				elif scaleOp == '-':
					modifiedSourceparamValue = sourceparamValue - scaleValue
				elif scaleOp == '**':
					modifiedSourceparamValue = sourceparamValue ** scaleValue
				else:
					raise ValueError("Unknown scale math op: '" + scaleOp + "'. Please give one of { *, /, +, -, ** }")

				# apply the scaled sourceparam to the targetparam:
				if   applyOp == 'mul':
					newvalue *= modifiedSourceparamValue
				elif applyOp == 'div':
					newvalue /= modifiedSourceparamValue
				elif applyOp == 'add':
					newvalue += modifiedSourceparamValue
				elif applyOp == 'sub':
					newvalue -= modifiedSourceparamValue
				elif applyOp == 'pow':
					newvalue **= modifiedSourceparamValue
				else:
					raise ValueError("Unknown apply math op: '"+applyOp+"'. Please give one of {mul,div,add,sub,pow}")

			#print "new value for '"+targetParamString+"': " + str(newvalue)
			setParamRecursively(targetParamString,newvalue,simparams)


def getShortParamString(paramdotpath):
	"""
	Get the short name of the param. This looses uniqueness of parameters (e.g. neurongroups.groupname.N), so should not be used for indexing!
	But sometimes, the long unique parameter name might just be too long...
	:param paramdotpath:
	:return:
	"""
	shortParamStringID = paramdotpath.rfind('.')
	return paramdotpath[shortParamStringID + 1:]


def getDependentParameterShortNameString(params,paramdotpath):

	shortParamString = getShortParamString(paramdotpath)

	if params.dependentParams.keys():
		shortParamCounter = 0

	# do the following for each defined dependent param:
	for targetParamString in params.dependentParams.keys():

		for operationTuple in params.dependentParams[targetParamString]:
			(applyOp, sourceParamString, scaleOp, scaleValue) = operationTuple

			# if this dependent param actually uses the given paramdotpath:
			if sourceParamString == paramdotpath:
				if shortParamCounter == 0:
					shortParamString += 'WITH'
				else:
					shortParamString += 'AND'
				shortParamString += getShortParamString(targetParamString)
				shortParamCounter += 1

	return shortParamString


def getReadableParamString(params,paramdotpath):
	
	dependentParamString = getDependentParameterShortNameString(params, paramdotpath)
	
	readableParamString = dependentParamString.replace('WITH',' (with ').replace('AND',' and ')
	readableParamString = readableParamString+')' if not readableParamString == dependentParamString else readableParamString

	return readableParamString


def insertParamStringIntoGroupString(paramGroupString, paramSubGroupString):
	""" One-liner not possible? So I split this up and made a function.
	This breaks apart the params string on the '_' separator, and inserts the new
	paramString at the proper position (so that cache files are unique). """
	if paramGroupString:
		tempList = paramGroupString.split('_')
		tempList.append(paramSubGroupString)
		tempList = sorted(tempList)
		combinedParamGroupString = '_'.join(tempList)
		return combinedParamGroupString
	else:
		return paramSubGroupString
	#return paramSubGroupString + '_' + paramGroupString

