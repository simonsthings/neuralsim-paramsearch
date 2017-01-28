#!/bin/python

import sys,os
import pickle

def main():
	try:
		relative_trialdir_path = sys.argv[1]
	except IndexError:
		relative_trialdir_path = "datafig/sim2017-01-20_trial5"

	if not os.path.exists(relative_trialdir_path):
		print "The given path was not found. Please specify an existing trial folder."
		sys.exit()

	pickled_params_filename =             relative_trialdir_path + '/data/settings_batch.pickle'
	alternative_pickled_params_filename = relative_trialdir_path +      '/settings_batch.pickle'
	if not os.path.exists(pickled_params_filename):
		print "The file '"+pickled_params_filename+"' could not be found. Using alternative folder."
		pickled_params_filename = alternative_pickled_params_filename
		if not os.path.exists(pickled_params_filename):
			print "The file '"+pickled_params_filename+"' could not be found. Please check this."
			sys.exit()
	else: # so if the pickle-file was found in its original location
		if not os.path.exists(pickled_params_filename):
			print "Pickle file found. Copying backup of pickle-file from '"+relative_trialdir_path+"/data' to '"+relative_trialdir_path+"'. "
			import shutil
			shutil.copyfile(pickled_params_filename, alternative_pickled_params_filename)
		
	print "Unpickling pickled parameters from '"+pickled_params_filename+"'..."
	with open(pickled_params_filename, 'r') as batchparamfile:
		pickled_params = pickle.load(batchparamfile)
		
	print pickled_params.keys()
	
	if pickled_params.runparams.pubscriptname == 'attractorEffectsOnSTDP':
		print "Generating figures via pubscript_attractorEffectsOnSTDP.make_figures(..)" # TODO: implement automatic discovery of which script was used to start the simulations. But logically also then git revision?
		import pubscript_attractorEffectsOnSTDP
		successful = pubscript_attractorEffectsOnSTDP.make_figures(pickled_params)
	elif pickled_params.runparams.pubscriptname == 'negDriftVersusGrowth':
		print "Generating figures via pubscript_negDriftVersusGrowth.make_figures(..)"  # TODO: implement automatic discovery of which script was used to start the simulations. But logically also then git revision?
		import pubscript_negDriftVersusGrowth
		successful = pubscript_negDriftVersusGrowth.make_figures(pickled_params)
	elif pickled_params.runparams.pubscriptname == 'projMultOrLearningrateWithMaxweight':
		print "Generating figures via pubscript_projMultOrLearningrateWithMaxweight.make_figures(..)"  # TODO: implement automatic discovery of which script was used to start the simulations. But logically also then git revision?
		import pubscript_projMultOrLearningrateWithMaxweight
		successful = pubscript_projMultOrLearningrateWithMaxweight.make_figures(pickled_params)
	else:  # pickled_params.runparams.pubscriptname == 'attractorEffectsOnSTDP':
		print "Defaulting to generating figures via pubscript_attractorEffectsOnSTDP.make_figures(..)" # TODO: implement automatic discovery of which script was used to start the simulations. But logically also then git revision?
		import pubscript_attractorEffectsOnSTDP
		successful = pubscript_attractorEffectsOnSTDP.make_figures(pickled_params)

	if not successful:
		print "There was a problem while generating the figures. The most likely reason for this is that not all parallel simulations have finished successfully. Re-starting the missing psims now!"
		
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

