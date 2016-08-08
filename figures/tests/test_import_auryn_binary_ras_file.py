import numpy as np
import matplotlib.pyplot as plt
from numpy import int32


def main():
	#fname = "sim_simon2.data/simon2_inputs.spk"
	#fname = '/Users/simon/Workspaces/WorkspaceGIT/MyGitHubAccount/auryn/plot/datafig/sim2016-08-02_trial10/data/psim_userecoveryFalse/repetition_1/sim2016-08-02_trial10_inputs.spk'
	fname = '/Users/simon/Workspaces/WorkspaceGIT/MyGitHubAccount/auryn/plot/datafig/sim2016-08-03_trial7/data/psim_userecoveryFalse/repetition_1/sim2016-08-03_trial7_inputs.spk'
	plotdata(fname)
	
	print ""
	
	#fname = "sim_simon2.data/simon2_outputs.spk"
	#plotdata(fname,True)
	
	plt.show()


def plotdata(fname, reshape=False):
	thedatatype = np.dtype([ ('time', int32) , ('neuronID',int32) ])
	print "Now loading data!"
	thedata = np.fromfile(fname, dtype=thedatatype)
	print "Finished loading the data!"
	print "Size of array: " + str(thedata.shape)
	print "Type of array: " + str(type(thedata))
	print "Contents of array: " + str(thedata)
	print "Contents of array field 0: " + str(thedata[0])
	print "Contents of array field 1: " + str(thedata[1])
	print "Contents of array field 2: " + str(thedata[2])
	print "Contents of array field 3: " + str(thedata[3])

	stepspersecond = thedata['time'][0]
	print "Steps per second: " + str(stepspersecond)
	dt = 1.0/stepspersecond
	print " -> stepsize: " + str(dt)
	
	if reshape:
		reshapeAndPlot(thedata,stepspersecond)
	else:
		#endplot = -1
		endplot = 5000 # 0.25 seconds
		endplot = 20/dt
		
		timespan = (0.5,1.0) # seconds

		inputrate=10 #Hz
		inputpopsize = 2000
		roughTimeScaler = inputpopsize * inputrate * stepspersecond/1000
		
		arrayspan = (timespan[0]*roughTimeScaler, timespan[1]*roughTimeScaler)
		print arrayspan
		
		plt.figure()
		#plt.plot(thedata['time'][1:endplot]*dt,thedata['neuronID'][1:endplot],'.')
		plt.plot(thedata['time'][arrayspan[0]:arrayspan[1]] * dt, thedata['neuronID'][arrayspan[0]:arrayspan[1]], '.')
		plt.axis('tight')
		plt.xlabel('time (s)')
		plt.ylabel('input units (#)')


def reshapeAndPlot(thedata,stepspersecond):
	
	simtime = 400 # seconds
	
	denseSpiketimes = np.zeros(simtime*stepspersecond)
	
	#endplot = -1
	endplot = 100000
	denseSpiketimes[thedata['time'][1:endplot]] = 1
	
	#print denseSpiketimes.shape
	patterninterval = 0.2 # 200 ms
	#denseSpiketimes.reshape((stepspersecond*patterninterval,-1))
	#np.reshape(denseSpiketimes,(stepspersecond*patterninterval,-1))
	#np.reshape(denseSpiketimes,(200,-1))
	denseSpiketimes = denseSpiketimes.reshape((-1,stepspersecond*patterninterval))
	print denseSpiketimes.shape
		
	(rows,cols) = np.nonzero(denseSpiketimes)
	print rows
	print cols
	
	plt.figure()
	#plt.imshow(denseSpiketimes, aspect='auto',interpolation='nearest')
	
	plt.plot(rows,cols,'.')
	
	pass
	
if __name__ == "__main__":
	main()

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		
		
		
		