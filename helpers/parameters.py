import numpy as np
from dotmap import DotMap
import os, sys
import matplotlib.pyplot as plt
from numpy import int32, arange
import peakutils





def extendParamSet_old(metaparams, baseParams, extendedParams, allsimparams, originalBaseParams=None,
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
                extendParamSet_old(metaparams, theBaseSubNodeObject, theExtendedSubNodeObject, allsimparams,
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

        # recursion! Do the same as below for the remaining params first:
        partialSimParams = crossAllParamsets(baseParams, flattenedExtendedParams ,[])

        for paramvalue in oneList:
            # change the given paramset at the given path
            for simparams in partialSimParams:
                setParamRecursively(onePath, paramvalue, simparams)

                # make a proper(?) copy of simparams struct and append it to allsimparams:
                newParams = DotMap(simparams.toDict())
                newParams.extendedparams[onePath] = paramvalue
                # print "A copy of baseParams was made and "
                # print " baseParams["+subnodepath+nodestring+"]="+str(originalBaseParams[subnodepath+nodestring])+" is now "
                # print "  newParams["+subnodepath+nodestring+"]="+str(newParams[subnodepath+nodestring])
                allsimparams.append(newParams)

        # print "Length of allsimparams before returning: " + str(len(allsimparams))
        return allsimparams


def splitByParameter(allsimparams,flattenedExtendedParams,paramStringsList):
    """
    This function groups parameter sets for each figure. Each new figure will be referenced by a new dict entry,
    where the key is a string of the figure name (with also contains any fixed parameter values per figure),
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

        shortPrarmStringID = oneParamString.rfind('.')
        shortParamString = oneParamString[shortPrarmStringID + 1:]

        perValueSimparams = {}

        #print "The param fullpath string: " + oneParamString
        #print "All values of this param: " + str(flattenedExtendedParams[oneParamString])

        for oneParamValue in flattenedExtendedParams[oneParamString]:
            #print "The Value: "+str(oneParamValue)

            newsimparamsList = []
            for simparams in allsimparams:
                if simparams.extendedparams[oneParamString] == oneParamValue:
                    newsimparamsList.append(simparams)
                    #allsimparams.remove(simparams)

            subdict = splitByParameter(newsimparamsList,flattenedExtendedParams,remainingParamStringsList)
            #thisPartialKey = shortParamString+str(oneParamValue)
            thisPartialKey = oneParamString+'='+str(oneParamValue)
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
