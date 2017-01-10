import dotmap
import numpy as np

# switch off the need for an X-windows backend:
import matplotlib as mpl
mpl.use('Agg')
#import matplotlib.pyplot as plt

import figures
import helpers


def define_extended_simulation_parameters(metaparams,baseParams):
	"""
	The helpers of baseParams that should be re-run with a list of settings each.
	Node paths of extendedParams have to match those in baseParams.
	"""

	extendedParams = dotmap.DotMap()
	#extendedParams.neurongroups.outputs.userecovery = [True,False]
	#extendedParams.neurongroups.inputs.rate = [ 10 , 15 ] # Hz
	#extendedParams.neurongroups.outputs.projMult = [ 1.0 , 1.5 , 1.8 ]
	#extendedParams.neurongroups.outputs.projMult = np.r_[0.2:4.2:0.2]
	#extendedParams.connectionsets.con1.stdprule.learningrate = 1/32.0 * np.array([0.5 , 1.0 , 2.0]) # eta in Auryn
	#extendedParams.connectionsets.con1.stdprule.learningrate = 1/32.0 * np.r_[0.2:4.2:0.2]
	#extendedParams.connectionsets.con1.maximumweight = np.array([0.5 , 1.0 , 2.0]) # eta in Auryn
	#extendedParams.connectionsets.con1.maximumweight = np.array([0.5 , 0.75 , 1.0 , 1.25 ,  1.5 , 1.75 , 2.0]) # eta in Auryn
	#extendedParams.connectionsets.con1.maximumweight = np.r_[0.2:4.2:0.2]
	#extendedParams.connectionsets.con1.maximumweight = np.r_[0.2:8.2:0.2]
	
	#extendedParams.connectionsets.con1.stdprule.weightdependence.attractorStrengthIndicator = [ 0.0 , 0.025 , 0.05 , 0.075 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5]
	#extendedParams.connectionsets.con1.stdprule.weightdependence.attractorStrengthIndicator = np.r_[0.0:0.52:0.025]
	extendedParams.connectionsets.con1.stdprule.weightdependence.attractorStrengthIndicator = np.linspace(0,1,num=21)
	
	#extendedParams.connectionsets.con1.stdprule.weightdependence.attractorLocationIndicator = np.linspace(-1,1,num=21)
	#extendedParams.connectionsets.con1.stdprule.weightdependence.attractorLocationIndicator = np.linspace(-1,1,num=41)
	#extendedParams.connectionsets.con1.stdprule.weightdependence.attractorLocationIndicator = np.r_[-0.2:0.4:0.1] # 7 values
	extendedParams.connectionsets.con1.stdprule.weightdependence.attractorLocationIndicator = np.round(np.r_[-0.2:0.4:0.05],3) # 13 values, rounded to 3 digits behind the dot

	extendedParams.connectionsets.con1.stdprule.weightdependence.theMeanSlope = np.linspace(0,0.6,num=4)

	#extendedParams.connectionsets.con1.stdprule.A_plus = [ 0.588 , 0.8 , 0.95 , 1.0 ]
	#extendedParams.connectionsets.con1.stdprule.A_plus = np.linspace( 0.2, 1.2, num=11)

	return extendedParams

def define_dependent_simulation_parameters():

	dependentParams = {}

	# key: path of dependent param. value: list of operations to compute the dependent param by:
	# value: ( source param path , math operation , value to apply )
	#dependentParams['connectionsets.con1.maximumweight'] = [ ('mul','connectionsets.con1.stdprule.learningrate' ,'*', 32.0) ]
	#dependentParams['connectionsets.con1.initialweight'] = [ ('mul','connectionsets.con1.stdprule.learningrate' ,'*', 32.0) ]

	#dependentParams['connectionsets.con1.initialweight'] = [ ('mul', 'connectionsets.con1.maximumweight' ,'*', 1.0) , ('mul', 'connectionsets.con1.stdprule.learningrate' ,'*', 32.0)]

	#dependentParams['connectionsets.con1.stdprule.learningrate'] = [ ('mul','connectionsets.con1.maximumweight' ,'*', 1.0) ]
	#dependentParams['connectionsets.con1.initialweight']         = [ ('mul','connectionsets.con1.maximumweight' ,'*', 1.0) ]

	return dependentParams


def define_base_simulation_parameters(metaparams):

	ms = 1e-3 # a millisecond.
	simparams = dotmap.DotMap()
	simparams.general.outfileprefix = metaparams.data_basename # dont need this: #+ "_repetition"+str(repetitionID+1)
	#simparams.general.testingProtocol.durations = [400]  #1500  #116  # seconds
	#simparams.general.testingProtocol.intervals = [0.2]  # patterns interval in seconds
	#simparams.general.testingProtocol.durations = [400,1000] # in seconds
	#simparams.general.testingProtocol.intervals = [0.2,10] # patterns interval in seconds
	simparams.general.testingProtocol.durations = [300,300,1500] # in seconds
	simparams.general.testingProtocol.intervals = [300,0.2,10] # patterns interval in seconds
	simparams.general.simtime = sum(simparams.general.testingProtocol.durations)
	simparams.recordings.detailedtracking = False

	simparams.neurongroups.inputs.N = 2000
	
	#simparams.neurongroups.inputs.type = "PoissonGroup"
	#simparams.neurongroups.inputs.type = "FileInputGroup"
	#simparams.neurongroups.inputs.type = "StructuredPoissonGroup"
	simparams.neurongroups.inputs.type = "PolychronousPoissonGroup"
	
	# only needed by PoissonGroup and StructuredPoissonGroup:
	simparams.neurongroups.inputs.rate = 10 # Hz
	simparams.neurongroups.inputs.randomseed = -1 # will be redefined in run_simulation()
	# only needed by FileInputGroup:
	simparams.neurongroups.inputs.rasfilename = '../sim_simon1.data/simon1_fileinputs.ras'
	# only needed by StructuredPoissonGroup and PolychronousPoissonGroup:
	simparams.neurongroups.inputs.patternduration = 100*ms
	simparams.neurongroups.inputs.patterninterval = 200*ms
	simparams.neurongroups.inputs.numberofstimuli = 1 # how many different patterns
	simparams.neurongroups.inputs.patternOccurrencesFilename = metaparams.data_basename+'_patterntimes.tiser'
	# only needed by PolychronousPoissonGroup:
	simparams.neurongroups.inputs.N_presenting = 600
	simparams.neurongroups.inputs.N_subpresenting = 600
	
	
	simparams.neurongroups.outputs.type = "Izhikevich2003Group"  # not used yet
	simparams.neurongroups.outputs.N = 1
	simparams.neurongroups.outputs.projMult = 1.0
	simparams.neurongroups.outputs.userecovery = False


	# Things to test:
	# projMult ; maxW ; learningrate ; input rate ; (STDP shape) ; (use_recovery) ; (dt) ; ...
	# input rate ; (STDP shape) ; (dt) ; ...


	simparams.connectionsets.con1.presynaptic = "inputs"
	simparams.connectionsets.con1.postsynaptic = "outputs"
	simparams.connectionsets.con1.initialweight = 0.85
	simparams.connectionsets.con1.maximumweight = 1.0
	#simparams.connectionsets.con1.type = "STDPConnection"
	#simparams.connectionsets.con1.type = "GeneralAlltoallSTDPConnection"
	simparams.connectionsets.con1.type = "WDHomeostaticSTDPConnection"

	simparams.connectionsets.con1.stdprule.A_plus = 0.8 # 0.588
	simparams.connectionsets.con1.stdprule.A_minus = -1
	simparams.connectionsets.con1.stdprule.tau_plus = 28.6 *ms
	simparams.connectionsets.con1.stdprule.tau_minus = 28.6 *ms #22e-3
	simparams.connectionsets.con1.stdprule.learningrate = 0.0325 *1 # eta in Auryn
		
#	simparams.connectionsets.con1.stdprule.A_plus = 1
#	simparams.connectionsets.con1.stdprule.A_minus = -0.85
#	simparams.connectionsets.con1.stdprule.tau_plus = 16.8 *ms
#	simparams.connectionsets.con1.stdprule.tau_minus = 33.7 *ms #22e-3
#	simparams.connectionsets.con1.stdprule.learningrate = 1/32.0/1.0 # eta in Auryn

	#simparams.connectionsets.con1.stdprule.weightdependence.type = "AdditiveWeightDependence"
	simparams.connectionsets.con1.stdprule.weightdependence.type = "LinearAttractorWeightDependence"
	simparams.connectionsets.con1.stdprule.weightdependence.attractorStrengthIndicator = 0.0
	simparams.connectionsets.con1.stdprule.weightdependence.attractorLocationIndicator = 0.5
	simparams.connectionsets.con1.stdprule.weightdependence.theMeanSlope = 0.0

	simparams.connectionsets.con1.homeostasis.type = "ConstantGrowth"
	simparams.connectionsets.con1.homeostasis.type = "RandomGrowth"
	simparams.connectionsets.con1.homeostasis.type = "RandomJitter"


	recordingparams = simparams.recordings
	recordingparams.inputs.samplinginterval_poprate = 0.1 # seconds
	recordingparams.outputs.samplinginterval_rate = 0.1 # seconds
	recordingparams.outputs.samplinginterval_membranes = 'dt' # seconds
	recordingparams.outputs.samplinginterval_ampa = 'dt' # seconds
	recordingparams.outputs.samplinginterval_nmda = 'dt' # seconds
	recordingparams.con1.samplinginterval_weightsum = 1 # seconds
	recordingparams.con1.samplinginterval_weightstats = 0.1 # seconds
	if simparams.general.simtime > 1000:
		recordingparams.con1.samplinginterval_weightmatrix = 10 # seconds
	elif simparams.general.simtime > 50:
		recordingparams.con1.samplinginterval_weightmatrix = 1 # seconds
	else:
		recordingparams.con1.samplinginterval_weightmatrix = 0.1 # seconds
	
	# recording times for TimespanMonitor:
	duration = 0.5
	membraneViews = [ 0 , 4 , 40 , simparams.general.simtime-1 ]
	recordingparams.dtintervalsAsFloats.starttimes = membraneViews
	recordingparams.dtintervalsAsFloats.stoptimes = (np.asarray(membraneViews) + duration).tolist()
	recordingparams.dtintervalsAsStrings.starttimes = ''
	recordingparams.dtintervalsAsStrings.stoptimes = ''
	
	for mi in xrange(len(membraneViews)):
		#recordingparams.dtintervalslist[mi].start = float(membraneViews[mi])
		#recordingparams.dtintervalslist[mi].stop = float(membraneViews[mi])+duration
		recordingparams.dtintervalsAsStrings.starttimes += str(float(membraneViews[mi])) + " "
		recordingparams.dtintervalsAsStrings.stoptimes  += str(float(membraneViews[mi] + duration)) + " "
			
			
	return simparams


def define_meta_parameters(existingSimfoldername=None):
	#### Define meta settings: executable, etc... ####
	basefolder = './datafig/'
	metaparams = dotmap.DotMap()
	#metaparams.executable_path = '../build/debug/examples/'
	#metaparams.executable_path = '../auryn_v0.8.0/build/release/examples/'
	#metaparams.executable_path = '../auryn_migration_to_v8.0/build/release/examples/'
	#metaparams.executable_file = 'sim_json'
	metaparams.executable_path = '' # use a symlink in the current folder:
	metaparams.executable_file = 'sim_json_symlink'
	if existingSimfoldername:
		metaparams.datafig_basename = existingSimfoldername
	else:
		metaparams.datafig_basename = helpers.simulation.find_unique_foldername(basefolder)
	metaparams.data_path = basefolder+metaparams.datafig_basename+'/data/'
	metaparams.data_basename = metaparams.datafig_basename
	metaparams.figures_path = basefolder+metaparams.datafig_basename+'/figures/'
	metaparams.figures_basename = metaparams.data_basename
	metaparams.numRepetitions = 4
	for repetitionID in xrange(metaparams.numRepetitions):
		metaparams.repetitionFoldernames[repetitionID] = 'repetition_'+str(repetitionID+1)
	return metaparams


def make_figures(params):
	try:
				
		figures.all_paramsets.figuretype_TwoParams2D_Accuracy.makeFig(params, paramdotpathX='connectionsets.con1.maximumweight', paramdotpathY='neurongroups.outputs.projMult')
		figures.all_paramsets.figuretype_TwoParams2D_Accuracy.makeFig(params, paramdotpathX='connectionsets.con1.stdprule.weightdependence.attractorLocationIndicator', paramdotpathY='connectionsets.con1.stdprule.weightdependence.attractorStrengthIndicator')
		#figures.all_paramsets.figuretype_TwoParams2D_Accuracy.makeFig(params, paramdotpathX='connectionsets.con1.stdprule.weightdependence.theMeanSlope', paramdotpathY='connectionsets.con1.stdprule.weightdependence.attractorStrengthIndicator')
		#figures.all_paramsets.figuretype_TwoParams2D_Accuracy.makeFig(params, paramdotpathX='connectionsets.con1.stdprule.weightdependence.attractorLocationIndicator', paramdotpathY='connectionsets.con1.stdprule.weightdependence.theMeanSlope')

		if params.baseParams.recordings.detailedtracking:
			# old: makeFigs(params.allsimparams,params.metaparams)
			figures.per_paramset.figuretype_FinalWeightsWithRepetitions.makeFigs(params)

			# if metaparams.numRepetitions < 5:
			# old: makeFigs(params.allsimparams,params.metaparams)
			if params.baseParams.general.simtime < 150 and params.metaparams.numRepetitions < 2:
				figures.per_repetition.figuretype_DevelopmentOfResponses.makeFigs(params,plotDevelopmentOfWeights=True)
			else:
				figures.per_repetition.figuretype_DevelopmentOfResponses.makeFigs(params,plotDevelopmentOfWeights=False)

		return True

	except IOError as e:
		print e.message
		print e
		print type(e)
		
		return False



def main():
	params = dotmap.DotMap()

	#### Define meta settings: executable, etc... ####
	existingSimfoldername = None
	#existingSimfoldername = 'sim2016-09-07_trial15'
	#existingSimfoldername = 'sim2016-09-07_trial17'
	#existingSimfoldername = 'sim2016-09-07_trial20'
	#existingSimfoldername = 'sim2016-09-08_trial1'
	#existingSimfoldername = 'sim2016-09-12_trial1'
	params.metaparams = define_meta_parameters(existingSimfoldername)
	
	##### Define simulation settings: ####
	params.baseParams = define_base_simulation_parameters(params.metaparams)
	params.extendedParams = define_extended_simulation_parameters(params.metaparams,params.baseParams)
	params.dependentParams = define_dependent_simulation_parameters()

	##### Rearrange them: #####
	params.flatParamLists = helpers.parameters.flattenExtendedParamsets(params.metaparams, params.baseParams, params.extendedParams)
	params.allsimparams = helpers.parameters.crossAllParamsets(params.baseParams, params.flatParamLists.copy())
	#nestedPrint(params.allsimparams)

	##### Update Dependent parameters: #####
	helpers.parameters.adjustDependentParameters(params)
	#nestedPrint(params.allsimparams)


	##### Run simulation(s) #####
	helpers.simulation.run_simulation(params, (existingSimfoldername==None) )
	
	#helpers.simulation.rerun_missing_simulations(params)
	
	##### Plot results #####
	#make_figures(params)


if __name__ == "__main__":
	main()

	
	
	
	
	
	
	

		
		
		
		