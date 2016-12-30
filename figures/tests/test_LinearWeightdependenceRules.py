"""
This file is a quick test to see how the linear weight dependence rules look plotted.
Also, transforming "theAttractorStrengthIndicator" and "theAttractorLocationIndicator" back into simple slopes and offsets.
This file does not invoke the actual simulator.
"""

import numpy as np
import matplotlib.pyplot as plt
import dotmap
import os


### From my C++ code:
#pWDUS->slope_Causal     = theMeanSlope- theAttractorStrengthIndicator;
#pWDUS->slope_Anticausal = theMeanSlope + theAttractorStrengthIndicator;
#pWDUS->offset_Causal = 0.5f - pWDUS->slope_Causal * theAttractorLocationIndicator;
#pWDUS->offset_Anticausal = 0.5f - pWDUS->slope_Anticausal * theAttractorLocationIndicator;


def translateRule(theAttractorStrengthIndicator, theAttractorLocationIndicator, theMeanSlope):
	params = dotmap.DotMap()
	
	params.slope_Causal     = theMeanSlope - theAttractorStrengthIndicator
	params.slope_Anticausal = theMeanSlope + theAttractorStrengthIndicator
	params.offset_Causal     = 0.5 - params.slope_Causal     * theAttractorLocationIndicator
	params.offset_Anticausal = 0.5 - params.slope_Anticausal * theAttractorLocationIndicator
	
	return params

def applyRule(ww, params):
	wd_LTP = params.slope_Causal * ww + params.offset_Causal
	wd_LTD = params.slope_Anticausal * ww + params.offset_Anticausal
	return (wd_LTP,wd_LTD)


def plotRule(S,L,M=0,newlocation = [0.1, 0.1, 0.5, 0.5]):
	params = translateRule(S, L, M)
	ww = np.linspace(-1, +1, 1001)
	(wd_LTP, wd_LTD) = applyRule(ww, params)
	# newlocation = [axesdims.figSpikes.x, axesdims.figSpikes.y1, axesdims.figSpikes.w, axesdims.figSpikes.h1]
	#newlocation = [0.1, 0.1, 0.5, 0.5]
	fig = plt.gcf()
	titlestring = 'S='+'{:1.2f}'.format(S)+', L='+'{:1.2f}'.format(L)+', M='+'{:1.2f}'.format(M)
	print titlestring
	ax = fig.add_axes(newlocation, title=titlestring)
	plt.plot(ww, wd_LTP, 'r',label='g_+(w)') # g_+(w)
	plt.plot(ww, wd_LTD, 'b',label='g_-(w)') # g_-(w)
	plt.xlim((0, 1))
	plt.ylim((0, 1))
	#plt.legend()


def main():
	
	allS = [0.1]
	#allS = np.linspace(0,0.5,6)
	#allL = np.linspace(-0.5,0.9,5)
	allS = np.linspace(0,0.5,num=4)
	allL = [0.1]
	#allL = np.r_[-0.2:0.4:0.1]  # 7 values
	#allM = [0.0]
	allM = np.linspace(0,0.5,num=4)
	
	leftoffset = 0.05
	rightoffset = 0.05
	bottomoffset = 0.05
	topoffset = 0.05
	wspace = 1-leftoffset-rightoffset
	hspace = 1-topoffset-bottomoffset
	wr = 0.8
	hr = 0.8
	for iS in xrange(len(allS)):
		for iL in xrange(len(allL)):
			for iM in xrange(len(allM)):
	
				#ypos = bottomoffset + hspace/len(allS) * iS
				#xpos = leftoffset   + wspace/len(allL) * iL
				#location = [xpos, ypos, wspace/len(allL)*wr, hspace/len(allS)*hr]

				#ypos = bottomoffset + hspace/len(allM) * iM
				#xpos = leftoffset   + wspace/len(allL) * iL
				#location = [xpos, ypos, wspace/len(allL)*wr, hspace/len(allM)*hr]

				ypos = bottomoffset + hspace/len(allS) * iS
				xpos = leftoffset   + wspace/len(allM) * iM
				location = [xpos, ypos, wspace/len(allM)*wr, hspace/len(allS)*hr]

				S = allS[iS]
				L = allL[iL]
				M = allM[iM]
				plotRule(S, L, M, location)
	
	plt.show()
	pass


if __name__ == "__main__":
	main()





