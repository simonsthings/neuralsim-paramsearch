import os
import random
import json
#from SimonsPythonHelpers import nestedPrint


def run_simulation(params ,wetRun=True):
	allsimparams = params.allsimparams
	metaparams = params.metaparams

	initialDir = os.path.abspath(os.curdir)
	if not os.path.exists(metaparams.data_path):
		os.makedirs(metaparams.data_path)
	os.chdir(metaparams.data_path)


	#theCmdString = ""
	theRedirectString = ""
	numParameterSets = len(allsimparams)
	if numParameterSets > 1 or metaparams.numRepetitions > 1:
		theRedirectString = ' 1> stdout.txt 2> stderr.txt'


	print "There are " +str(len(params.flatParamLists.keys()))+" parameter sets to be evaluated:"
	for flatParamString in params.flatParamLists.keys():
		paramList = params.flatParamLists[flatParamString]
		print '- ' + flatParamString + ': ' + str(len(paramList)) + ' values'

	print "Also, " +str(len(params.dependentParams.keys()))+" parameters depend on others:"
	for dependentParamString in params.dependentParams.keys():
		paramList = params.dependentParams[dependentParamString]
		print '- ' + dependentParamString + ': ' + str(paramList) + ' '

	summaryText = "Now running " \
			  + str(numParameterSets * metaparams.numRepetitions) \
			  + " parallel jobs, consisting of " \
			  + str(numParameterSets) \
			  + " parameter sets with " \
			  + str(metaparams.numRepetitions) \
			  + " repetitions each."

	if numParameterSets > 1:
		print summaryText + " Screen output redirected to stdout.txt and stderr.txt to avoid terminal confusion."
	else:
		print summaryText + " Showing screen output here."





	if wetRun:

		parjobfile = open('par_jobs.txt', 'w')
		print "Preparing result folder structure and writing to " + metaparams.data_path + parjobfile.name
		
		for paramsetID in xrange(numParameterSets):
			simparams = allsimparams[paramsetID]
			produceExtendedparamFoldername(simparams)
			if not os.path.exists(simparams.extendedparamFoldername):
				os.makedirs(simparams.extendedparamFoldername)
			os.chdir(simparams.extendedparamFoldername)
	
			for repetitionID in xrange(metaparams.numRepetitions):
				repfolder = metaparams.repetitionFoldernames[repetitionID]
				if not os.path.exists(repfolder):
					os.makedirs(repfolder)
				
				simparams.repetitionID = repetitionID
				simparams.neurongroups.inputs.randomseed = int(random.randint(0, 2 ** 30))  # long(time.time())
				#simparams.neurongroups.inputs.randomseed = 1043771618
				paramfile = open(repfolder + '/settings_simulation.json', 'w')
				json.dump(simparams.toDict(), paramfile, sort_keys=True, indent=4, separators=(',', ': '))
				paramfile.close()
	
				# paramfile = open(metaparams.data_path+'settings_recording.json', 'w')
				# json.dump(oneSimParams.recordings.toDict(), paramfile, sort_keys=True, indent=4, separators=(',', ': '))
				# paramfile.close()
	
				# if (repetitionID+1 == metaparams.numRepetitions) and (paramsetID+1 == numParameterSets):
				#    theRedirectString = ""
	
				#theCmdString += "( cd " + metaparams.data_path+simparams.extendedparamFoldername + '/' + repfolder + " ; " + initialDir +'/'+ metaparams.executable_path + metaparams.executable_file + ' --settingsfile ' + os.getcwd() + '/' + repfolder + '/settings_simulation.json ' + theRedirectString + '; cd '+initialDir+' ) &'
	
				simString = " cd " + initialDir+'/'+metaparams.data_path+simparams.extendedparamFoldername + '/' + repfolder + " ; " + initialDir +'/'+ metaparams.executable_path + metaparams.executable_file + ' --settingsfile ' + os.getcwd() + '/' + repfolder + '/settings_simulation.json ' + theRedirectString + '; cd '+initialDir+'  \n'
				parjobfile.write(simString)
	
			os.chdir('..')
	
		#theCmdString += "time wait "
	
		# os.system('time ../'+sim_executable_path+sim_executable_file+' '+' --seed='+str(simparams.neurongroups.inputs.randomseed)+' --simtime='+str(simparams.general.simtime)+' --Npre='+str(simparams.neurongroups.inputs.N)+' ')
		# os.system('time ../'+sim_executable_path+sim_executable_file+' '+'  ')
		# os.system('time ../'+sim_executable_path+sim_executable_file+' --show-settings'+'  ')
		# os.system('time ../'+sim_executable_path+sim_executable_file+' --show-settings --settingsfile /Users/simon/Workspaces/WorkspaceGIT/MyGitHubAccount/auryn/plot/sim_simon1.data/settings_simulation.json '+'  ')
		# os.system('time ../'+sim_executable_path+sim_executable_file+' --show-settings --settingsfile '+os.getcwd()+'/settings_simulation.json '+'  ')
		# os.system('time ../'+sim_executable_path+sim_executable_file+' --settingsfile '+os.getcwd()+'/settings_simulation.json '+'  ')
		# print "The command string is:"
		# print theCmdString
	
		parjobfile.close()
		
		# export everything to its own pickled file, just in case. This will usually never be read again and is just for debugging:
		print "Saving the whole gobbledigook of batch-params via pickle, just in case..."
		import pickle
		params.runparams.pubscriptname = __get_pubscript_name()
		batchparamfile = open('settings_batch.pickle', 'w')
		pickle.dump(params,batchparamfile,protocol=2)  # protocol 2 should be a compressed, binary format.
		batchparamfile.close()
		
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

		print "Now actually running sims. Writing data to '"+params.metaparams.datafig_basename+"'..."
		__run_local_or_on_cluster('par_jobs.txt', numSimulations=numParameterSets * metaparams.numRepetitions)
	else:
		print "Skipping sims! (Using data in '"+params.metaparams.datafig_basename+"' instead!)"  # dry run
		
		# Insert extendedparamFoldername and repetitionID into each simparams set, because some figure generation scripts refer to them
		# (could also read the random seed from json file, but that is unnecessary and would be slow):
		for paramsetID in xrange(numParameterSets):
			simparams = allsimparams[paramsetID]
			produceExtendedparamFoldername(simparams)
			for repetitionID in xrange(metaparams.numRepetitions):
				simparams.repetitionID = repetitionID

	os.chdir(initialDir)

	pass


def produceExtendedparamFoldername(simparams):
	paramsetFoldername = 'psim'
	shortParamStrings = {}
	for psimParamString in simparams.extendedparams:  # make a dict of just the last part of each param string
		if '.' in psimParamString:
			lastDotPosition = psimParamString.rfind('.')
			shortParamStrings[psimParamString[lastDotPosition + 1:]] = psimParamString
		else:
			shortParamStrings[psimParamString] = psimParamString
	for shortParamString in sorted(shortParamStrings.keys()):  # sort that dict's keys and create folder name of params in alphabetical order.
		psimParamString = shortParamStrings[shortParamString]
		paramsetFoldername += '_' + shortParamString + str(simparams.extendedparams[psimParamString])
	simparams.extendedparamFoldername = paramsetFoldername


def find_unique_foldername(basefolder='', repeatLastName=False):
	import datetime
	import os, glob
	
	if not os.path.exists(basefolder):
		os.makedirs(basefolder)
		
	oldpath = str(os.path.abspath(os.curdir))
	os.chdir(basefolder)
		
	daystamp = 'sim'+str(datetime.date.today())
	daylist = glob.glob(daystamp + '*')
	#daylist = glob.glob('*')
	
	largestID = 0
	if daylist:
		for foldername in daylist:
			lastdotID = str(foldername).rfind('.')
			## stopped using dot-separator for data vs figures dirs. Now just using subdirs. But need an if clause because of that now:
			if lastdotID > 0:
				trialIDstring = foldername[len(daystamp)+len('_trial'):lastdotID]
			else:
				trialIDstring = foldername[len(daystamp)+len('_trial'):]
			largestID = max(largestID,int(trialIDstring))
	#else:
		#print "no files matching '"+daystamp+"' found in "+ str(os.path.abspath(os.curdir))

	if repeatLastName:
		uniquename = daystamp + '_trial' + str(largestID + 0)
	else:
		uniquename = daystamp + '_trial' + str(largestID + 1)

	#os.mkdir(uniquename+'.data')
	#os.mkdir(uniquename+'.figures')

	os.chdir(oldpath)
	return uniquename



def rerun_missing_simulations(params,wetRun=True):
		
	initialDir = os.path.abspath(os.curdir)
	os.chdir(params.metaparams.data_path)

	missingparjobfile = open('par_jobs_repeatmissing.txt', 'w')

	missing_counter = 0
	with open('par_jobs.txt', 'r') as parjobfile:
		for line in parjobfile:
			startString = '--settingsfile '
			endString = 'settings_simulation.json'
			resultsfolderpathStart = line.find(startString)
			resultsfolderpathEnd = line.rfind(endString)
			resultsfolderPath = line[(resultsfolderpathStart+len(startString)):resultsfolderpathEnd]
			
			if not os.path.isfile(resultsfolderPath+params.metaparams.datafig_basename+'.stimulusdetectionstatistics.txt'):
				print resultsfolderPath + ' has no file called "'+params.metaparams.datafig_basename+'.stimulusdetectionstatistics.txt". '
				missingparjobfile.write(line)
				missing_counter += 1
	
	missingparjobfile.close()
	
	
	if wetRun:
		if missing_counter>0:
			print "Now re-running "+str(missing_counter)+" sims of '"+params.metaparams.datafig_basename+"' that somehow didn't succeed in the first run..."
			
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
			
			__run_local_or_on_cluster('par_jobs_repeatmissing.txt', numSimulations=missing_counter)

	os.chdir(initialDir)

	pass

def __get_pubscript_name():
	import traceback
	try:
		raise ValueError
	except:
		tb = traceback.extract_stack()
		for se in tb:
			if 'pubscript_' in se[0]:
				pubscriptPos = str(se[0]).rfind('_') + 1
				pubscriptname = se[0][pubscriptPos:-3]
				return pubscriptname
	return 'neuralsim'

def __run_local_or_on_cluster(jobfilename, numSimulations=None,anyemailnotificationsettings=' -m bea  -M simon.vogt@blbt.uni-freiburg.de '):
	if not numSimulations:
		# this code is untested. May over- or undercount by 1.
		i=0
		with open(jobfilename) as f:
			for i, l in enumerate(f):
				pass
		numSimulations = i + 1
	numJobs = min(numSimulations,3000)
	
	scriptnamepath = os.path.realpath(__file__)
	scriptpath = scriptnamepath[:scriptnamepath.rfind('/')]
	#print scriptpath
	
	theHostname = ''
	if 'HOSTNAME' in os.environ.keys():
		theHostname = os.environ['HOSTNAME']
	
	if '.nemo.' in theHostname and numSimulations > 30:
		# running on the bwFor-NEMO cluster!
		moabJobname = __get_pubscript_name()
		moabCmdString = 'msub '+anyemailnotificationsettings+' -v JOBLISTFILE="'+jobfilename+'" -t '+moabJobname+'[1-'+str(numJobs) + '] '+scriptpath+'/moab_arrayrun.sh >> moab_jobid.txt'
		print moabCmdString
		# reset the progress counter, to be re-built by moab_arrayrun.sh:
		try:
			os.remove("psims_started.txt")
			os.remove("psims_finished.txt")
		except OSError:
			pass  # ignore any errors: they probably just mean that the file hadn't been created yet.
		os.system(moabCmdString)
		os.system("cat moab_jobid.txt")  # quick way to both display the job id on the terminal as well as writing it to a file (see moabCmdString).
		pass
	elif 'automatix' in theHostname and numSimulations > 30:
		# running on automatix.nes.uni-freiburg.de
		pass
	else:
		# running locally using gnu-parallel (gnu-parallel must be installed on this machine):
		gnuParallelCmdString = "time parallel --bar --joblog " + os.getcwd() + "/joblog_missing.txt :::: " + jobfilename
		print gnuParallelCmdString
		os.system(gnuParallelCmdString)
		pass