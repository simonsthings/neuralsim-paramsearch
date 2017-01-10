#!/bin/python

import sys,os
import pickle

def main():
	relative_trialdir_path = sys.argv[1]

	if not os.path.exists(relative_trialdir_path):
		print "The given path was not found. Please specify an existing trial folder."
		sys.exit()

	pickled_params_filename = relative_trialdir_path + '/data/settings_batch.pickle'
	if not os.path.exists(pickled_params_filename):
		print "The file '"+pickled_params_filename+"' could not be found. Please check this."
		sys.exit()
	
	with open(pickled_params_filename, 'r') as batchparamfile:
		pickled_params = pickle.load(batchparamfile)
		
	print pickled_params.keys()
	
	print "Generating figures via pubscript_attractorEffectsOnSTDP.make_figures(..)" # TODO: implement automatic discovery of which script was used to start the simulations. But logically also then git revision?
	import pubscript_attractorEffectsOnSTDP
	successful = pubscript_attractorEffectsOnSTDP.make_figures(pickled_params)

	if not successful:
		print "There was a problem while generating the figures. The most likely reason for this is that not all parallel simulations have finished successfully. Re-starting the missing psims now!"
		
		import time
		print "Starting simulation in 5 seconds..."
		time.sleep(1)
		print "4"
		time.sleep(1)
		print "3"
		time.sleep(1)
		print "2"
		time.sleep(1)
		print "1"
		time.sleep(1)

		import helpers
		helpers.simulation.rerun_missing_simulations(pickled_params)

	else:
		# everything finished successfully. Do some cleaning!
		print "Finished generating all figures. Now cleaning up some temporary files in '"+ relative_trialdir_path +"/data' ..."
		os.chdir(relative_trialdir_path+'/data')
		
		tarCmd = "tar czf moab_terminaloutputs.tar.gz attractorEffectsOnSTDP.*"
		print tarCmd
		os.system(tarCmd)
		
		rmCmd = "rm attractorEffectsOnSTDP.o* attractorEffectsOnSTDP.e*"
		print rmCmd
		os.system(rmCmd)

if __name__ == "__main__":
		main()

