import numpy as np
import matplotlib.pyplot as plt
from dotmap import DotMap
from SimonsPythonHelpers import nestedPrint
import time
import json
import os

def main():
	
	#sim_executable_path = '../../build/debug/examples/'
	sim_executable_path = '~/.auryn-local/auryn_migration_to_v8.0/build/release/examples/'
	sim_executable_file = 'test_Izhikevich2003Group'
	sim_data_path = './'+sim_executable_file+'.data/'
	sim_data_basename = 'test_Izhi'
	sim_figures_path = './'+sim_executable_file+'.figures/'
	sim_figures_basename = sim_data_basename


	ms = 1e-3
	
	#timespan = ( 0.0 , 1.0 )
	#timespan = ( 0.0 , 0.1 )
	timespan = ( 1.0 , 1.1 )
	#timespan = ( 0.0 , 2.0 )

	print "Using '"+sim_executable_file+"' as executable..."
	run_simulation(sim_executable_path,sim_executable_file,sim_data_path)

	
	axesdims = DotMap()
	axesdims.figSpikes.x = 0.1
	axesdims.figSpikes.w = 0.85
	axesdims.figSpikes.y1 = 0.75  # input currents
	axesdims.figSpikes.h1 = 0.2   # input currents
	axesdims.figSpikes.y2 = 0.05  # membranes
	axesdims.figSpikes.h2 = 0.3   # membranes
	axesdims.figSpikes.y3 = 0.1   # output raster
	axesdims.figSpikes.h3 = 0.05  # output rater
	axesdims.figSpikes.y4 = 0.4  #
	axesdims.figSpikes.h4 = 0.1   #
	axesdims.figSpikes.y5 = 0.45   # recovery
	axesdims.figSpikes.h5 = 0.2  # recovery
	
	axesdims.figWeights.x1 = 0.1
	axesdims.figWeights.w1 = 0.9
	axesdims.figWeights.x2 = None  # will be set below!
	axesdims.figWeights.w2 = None  # will be set below!
	axesdims.figWeights.y1 = 0.25
	axesdims.figWeights.h1 = 0.55
	axesdims.figWeights.y2 = 0.9  # rate
	axesdims.figWeights.h2 = 0.05  # rate
	axesdims.figWeights.y3 = 0.05  # stats!
	axesdims.figWeights.h3 = 0.05  # stats!
	
	#nestedPrint(axesdims)

	if True:
		os.system('mkdir -p '+sim_figures_path)
	
	
	
	simdata = getSimData(sim_data_path+sim_data_basename)


	print "Now drawing membrane and raster plot figure for timespan " + str(timespan) + ""
	figSpikesAndMembranes = plt.figure()
	inputcurrents(axesdims,simdata,timespan)  # can't currently be tracked due to order of recording and resetting in auryn.
	recovery(axesdims,simdata,timespan)
	membranes(axesdims,simdata,timespan)
	outputraster(axesdims,simdata,timespan)
	figSpikesAndMembranes.savefig(sim_figures_path+sim_figures_basename+'_SpikesAndMembranes.png')
	#plt.show() ; exit()




def run_simulation(sim_executable_path,sim_executable_file,sim_data_path):
	os.system('mkdir -p '+sim_data_path)
	os.chdir(sim_data_path)
	os.system('time '+sim_executable_path+sim_executable_file+' '+'  ')
	os.chdir('..')
	
def getSingleDatatrail(filename, columnNames):
	if os.path.isfile(filename) and os.path.getsize(filename) > 0:
		try:
			datatrail = np.genfromtxt(filename,
									names=columnNames,
									comments='#',    # skip comment lines
									dtype = None)    # guess dtype of each column
		except Exception as e:
			print "Oh-oh! There was an exception: " + str(e)
			print "The type of it was: " + str(type(e))
			exit()
	else:
		if not os.path.isfile(filename):
			print "The file '"+filename+"' does not exist. Skipping."
		else:
			print "The file '"+filename+"' is empty. Skipping."
		datatrail = []

	return datatrail
	
def getSimData(datafile_basename):
	simdata = {}
	print "Loading RAS..."
	simdata['output_raster'] = getSingleDatatrail(datafile_basename+'.ras.txt', "time,nodeID")
	print "Loading Membrane data..."
	simdata['membranes'] = getSingleDatatrail(datafile_basename+'.mem.txt', "time,mempot")
	print "Loading recovery U data..."
	simdata['recovery'] = getSingleDatatrail(datafile_basename+'.u.txt', "time,recov")
	if 1:
		print "Loading excitatory input ampa conductance data..."
		simdata['inputcurrents'] = getSingleDatatrail(datafile_basename+'.g_ampa.txt', "time,t_exc")
	else:
		print "Loading excitatory input currents data..."
		simdata['inputcurrents'] = getSingleDatatrail(datafile_basename+'.t_exc.txt', "time,t_exc")
	return simdata



def inputcurrents(axesdims, theSimdata, timespan=None):
	datatrail = theSimdata['inputcurrents']
	
	newlocation = [axesdims.figSpikes.x, axesdims.figSpikes.y1, axesdims.figSpikes.w, axesdims.figSpikes.h1]
	fig = plt.gcf()
	ax = fig.add_axes(newlocation, title='input currents')
	
	# print(simdata)
	if timespan:
		indexes = (datatrail['time'] > timespan[0]) & (datatrail['time'] < timespan[1])
		plt.plot(datatrail['time'][indexes], datatrail['t_exc'][indexes])
	# plt.plot(datatrail[-1000:,0],datatrail[-1000:,1],'-')
	else:
		plt.plot(datatrail['time'], datatrail['t_exc'])
	
	if timespan:
		plt.xlim(timespan)
	else:
		fulltimespan = (0, theSimdata['inputcurrents'][-1][0])
		plt.xlim(fulltimespan)
	
	theYlim = plt.ylim()
	ylimOffset = (theYlim[1] - theYlim[0]) * 0.1
	plt.ylim([theYlim[0] - ylimOffset, theYlim[1] + ylimOffset])


def recovery(axesdims,theSimdata,timespan=None):
	datatrail = theSimdata['recovery']
	
	newlocation = [axesdims.figSpikes.x,axesdims.figSpikes.y5,axesdims.figSpikes.w,axesdims.figSpikes.h5]
	fig = plt.gcf()
	ax = fig.add_axes(newlocation,title='recovery variable U')
	
	#print(simdata)
	if timespan:
		indexes = (datatrail['time'] > timespan[0]) & (datatrail['time'] < timespan[1])
		plt.plot(datatrail['time'][indexes],datatrail['recov'][indexes])
		#plt.plot(datatrail[-1000:,0],datatrail[-1000:,1],'-')
	else:
		plt.plot(datatrail['time'],datatrail['recov'])

	if timespan:
		plt.xlim(timespan)
	else:
		fulltimespan = (0 , theSimdata['recovery'][-1][0])
		plt.xlim(fulltimespan)
	#theYLims = plt.ylim()
	#plt.ylim([-0.08,0.04])
	#plt.ylim([-0.04,0.12])
	#plt.ylim([-0.02,0.1])

	theYlim = plt.ylim()
	ylimOffset = (theYlim[1] - theYlim[0]) * 0.1
	plt.ylim([theYlim[0]-ylimOffset,theYlim[1]+ylimOffset])
	
	#theYticks = ax.get_yticks()
	#newYticks = [theYticks[0],theYticks[-1]]
	##newYticks = [theYticks[0],0,theYticks[-1]]
	#ax.set_yticks(newYticks)

	
def membranes(axesdims,theSimdata,timespan=None):
	datatrail = theSimdata['membranes']
		
	mV=1e-3

	newlocation = [axesdims.figSpikes.x,axesdims.figSpikes.y2,axesdims.figSpikes.w,axesdims.figSpikes.h2]
	fig = plt.gcf()
	ax = fig.add_axes(newlocation,title='membrane potentials')
	
	# Crop large membranes:
	datatrail['mempot'][datatrail['mempot'] > 30*mV] = 30*mV
	
	#print(simdata)
	if timespan:
		indexes = (datatrail['time'] > timespan[0]) & (datatrail['time'] < timespan[1])
		plt.plot(datatrail['time'][indexes],datatrail['mempot'][indexes]/mV)
		#plt.plot(datatrail[-1000:,0],datatrail[-1000:,1],'-')
	else:
		plt.plot(datatrail['time'],datatrail['mempot']/mV)

	if timespan:
		plt.xlim(timespan)
	else:
		fulltimespan = (0 , theSimdata['membranes'][-1][0])
		plt.xlim(fulltimespan)
	#theYLims = plt.ylim()
	#plt.ylim([-0.08,0.04])
	#plt.ylim([-0.04,0.12])
	#plt.ylim([-0.02,0.1])
	
	theYlim = plt.ylim()
	ylimOffset = (theYlim[1] - theYlim[0]) * 0.1
	plt.ylim([theYlim[0]-ylimOffset,theYlim[1]+ylimOffset])
	
	#theYticks = ax.get_yticks()
	#newYticks = [theYticks[0],theYticks[-1]]
	##newYticks = [theYticks[0],0,theYticks[-1]]
	#ax.set_yticks(newYticks)
	
	plt.ylabel("voltage (mV)")

	

def outputraster(axesdims,theSimdata,timespan=None):
	datatrail = theSimdata['output_raster']
	
	y_dataoffset = 35
	
	newlocation = [axesdims.figSpikes.x,axesdims.figSpikes.y3,axesdims.figSpikes.w,axesdims.figSpikes.h3]
	fig = plt.gcf()
	#ax = fig.add_axes(newlocation,title='output spike raster')
	ax = plt.gca()

	print datatrail
	print type(datatrail)
	if type(datatrail) is not list:
		print datatrail.shape
		print datatrail.size
		#print datatrail[0]
		#print datatrail[1]
	
	if type(datatrail) is list or datatrail.size == 0:
		print "There are no output spikes to print. Skipping the output spike raster plot of this figure."
		plt.title('no output spikes')
		return

	if timespan:
		indexes = (datatrail['time'] > timespan[0]) & (datatrail['time'] < timespan[1])
	else:
		indexes = np.arange(len(datatrail))
		#plt.plot(datatrail['time'],datatrail['nodeID'],'.k')
	plt.plot(datatrail['time'][indexes],y_dataoffset+datatrail['nodeID'][indexes],'.k')
	
	if timespan:
		plt.xlim(timespan)
	else:
		fulltimespan = (0 , theSimdata['membranes'][-1][0])
		plt.xlim(fulltimespan)
	ax.set_xlabel('time (s)');

	#theYticks = ax.get_yticks()
	#newYticks = [theYticks[0],theYticks[-1]]
	#ax.set_yticks(newYticks)
	
	

	
if __name__ == "__main__":
	main()

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		
		
		
		