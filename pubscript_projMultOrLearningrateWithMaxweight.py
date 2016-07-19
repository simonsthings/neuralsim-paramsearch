import os
import numpy as np
import dotmap
from SimonsPythonHelpers import nestedPrint

from helpers.parameters import flattenExtendedParamsets, crossAllParamsets
from helpers.simulation import run_simulation

#from figures.figuretype_OneParamAndRepetitions_Accuracy import makeFig
from figures.repetitiondetail import make_singlerun_figures
from figures.repetitionsummary import make_repetitionsummary_figures
import figures

def define_extended_simulation_parameters(metaparams,baseParams):
    """
    The helpers of baseParams that should be re-run with a list of settings each.
    Node paths of extendedParams have to match those in baseParams.
    """

    extendedParams = dotmap.DotMap()
    extendedParams.neurongroups.outputs.userecovery = [True,False]
    #extendedParams.neurongroups.inputs.rate = [ 10 , 15 ] # Hz
    extendedParams.neurongroups.outputs.projMult = np.r_[0.2:4.2:0.2]
    #extendedParams.neurongroups.outputs.projMult = np.r_[0.2:2.2:0.2]
    #extendedParams.neurongroups.outputs.projMult = np.r_[2.2:4.2:0.2]
    #extendedParams.neurongroups.outputs.projMult = [ 1.0 , 1.5 , 1.8 ]

    #extendedParams.connectionsets.con1.stdprule.learningrate = 1/32.0 * np.array([0.5 , 1.0 , 2.0]) # eta in Auryn
    ##extendedParams.connectionsets.con1.stdprule.learningrate = 1/32.0 * np.r_[0.2:4.2:0.2]

    return extendedParams


def define_base_simulation_parameters(metaparams):

    ms = 1e-3 # a millisecond.
    simparams = dotmap.DotMap()
    simparams.general.outfileprefix = metaparams.data_basename # dont need this: #+ "_repetition"+str(repetitionID+1)
    simparams.general.testingProtocol_durations = [ 200 ]  #1500  #116
    simparams.general.testingProtocol_phasetypes = [1]  # 0=noise, 1=patterns, 2=test type A, 3=test type B, ...
    #simparams.general.testingProtocol_durations = [300,300,900] # in seconds
    #simparams.general.testingProtocol_phasetypes = [0,1,3] # 0=noise, 1=patterns, 2=test type A, 3=test type B, ...
    simparams.general.simtime = sum(simparams.general.testingProtocol_durations)
    simparams.recordings.detailedtracking = True

    simparams.neurongroups.inputs.N = 2000
    
    #simparams.neurongroups.inputs.type = "PoissonGroup"
    #simparams.neurongroups.inputs.type = "FileInputGroup"
    #simparams.neurongroups.inputs.type = "StructuredPoissonGroup"
    simparams.neurongroups.inputs.type = "PolychronousPoissonGroup"
    
    # only needed by PoissonGroup and StructuredPoissonGroup:
    simparams.neurongroups.inputs.rate = 10 # Hz
    simparams.neurongroups.inputs.randomseed = 1459350219 # will be redefined in run_simulation()
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
    
    
    simparams.neurongroups.outputs.type = "IzhikevichGroup"  # not used yet
    simparams.neurongroups.outputs.N = 1
    simparams.neurongroups.outputs.projMult = 1.5
    simparams.neurongroups.outputs.userecovery = False


    # Things to test:
    # projMult ; maxW ; learningrate ; input rate ; (STDP shape) ; (use_recovery) ; (dt) ; ...


    simparams.connectionsets.con1.presynaptic = "inputs"
    simparams.connectionsets.con1.postsynaptic = "outputs"
    simparams.connectionsets.con1.initialweight = 0.85
    simparams.connectionsets.con1.maximumweight = 1.0

#     simparams.connectionsets.con1.stdprule.A_plus = 0.588
#     simparams.connectionsets.con1.stdprule.A_minus = -1
#     simparams.connectionsets.con1.stdprule.tau_plus = 28.6 *ms
#     simparams.connectionsets.con1.stdprule.tau_minus = 28.6 *ms #22e-3
#     simparams.connectionsets.con1.stdprule.learningrate = 0.0325 *1 # eta in Auryn
        
    simparams.connectionsets.con1.stdprule.A_plus = 1
    simparams.connectionsets.con1.stdprule.A_minus = -0.85
    simparams.connectionsets.con1.stdprule.tau_plus = 16.8 *ms
    simparams.connectionsets.con1.stdprule.tau_minus = 33.7 *ms #22e-3
    simparams.connectionsets.con1.stdprule.learningrate = 1/32.0/1.0 # eta in Auryn


    
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
    
    # possible future feature?:
    duration = 0.5;
    membraneViews = [ 0 , 4 , 40 , simparams.general.simtime-1 ]
    recordingparams.dtintervalsAsFloats.starttimes = membraneViews
    recordingparams.dtintervalsAsFloats.stoptimes = (np.asarray(membraneViews) + duration).tolist()
    recordingparams.dtintervalsAsStrings.starttimes = ''
    recordingparams.dtintervalsAsStrings.stoptimes = ''
    
    for mi in xrange(len(membraneViews)):
        #recordingparams.dtintervalslist[mi].start = float(membraneViews[mi])
        #recordingparams.dtintervalslist[mi].stop = float(membraneViews[mi])+duration
        recordingparams.dtintervalsAsStrings.starttimes += str(float(membraneViews[mi])) + " ";
        recordingparams.dtintervalsAsStrings.stoptimes  += str(float(membraneViews[mi] + duration)) + " ";
            
            
    return simparams


def define_meta_parameters():
    #### Define meta settings: executable, etc... ####
    metaparams = dotmap.DotMap()
    metaparams.executable_path = '../build/debug/examples/'
    metaparams.executable_file = 'sim_simon5'
    metaparams.data_path = './datafig/'+metaparams.executable_file+'.data/'
    metaparams.data_basename = 'simon5'
    metaparams.figures_path = './datafig/'+metaparams.executable_file+'.figures/'
    metaparams.figures_basename = metaparams.data_basename
    metaparams.numRepetitions = 1
    for repetitionID in xrange(metaparams.numRepetitions):
        metaparams.repetitionFoldernames[repetitionID] = 'repetition_'+str(repetitionID+1)
    return metaparams


def make_figures(params):
    try:

        os.system( 'mkdir -p ' +params.metaparams.figures_path)

        # figures.makeFiguretype_TwoParamImage_Accuracy(params,paramStringX='connectionsets.con1.weightdependence.attractorLocation',paramStringY='connectionsets.con1.weightdependence.attractorStrength')
        figures.makeFiguretype_OneParamAndRepetitions_Accuracy(params, paramString='neurongroups.outputs.projMult')
        figures.makeFiguretype_OneParamAndRepetitions_Accuracy(params, paramString='connectionsets.con1.stdprule.learningrate')


        if params.baseParams.recordings.detailedtracking:
            make_repetitionsummary_figures(params.allsimparams,params.metaparams)

            # if metaparams.numRepetitions < 5:
            make_singlerun_figures(params.allsimparams,params.metaparams)


    except IOError as e:
        print e.message
        print e
        print type(e)



def main():
    params = dotmap.DotMap()

    #### Define meta settings: executable, etc... ####
    params.metaparams = define_meta_parameters()

    ##### Define simulation settings: ####
    params.baseParams = define_base_simulation_parameters(params.metaparams)
    params.extendedParams = define_extended_simulation_parameters(params.metaparams,params.baseParams)

    ##### Rearrange them: #####
    params.flatParamLists = flattenExtendedParamsets(params.metaparams, params.baseParams, params.extendedParams)
    params.allsimparams = crossAllParamsets(params.baseParams, params.flatParamLists.copy())
    #nestedPrint(allsimparams)


    ##### Run simulation(s) #####
    run_simulation(params, False)


    ##### Plot results #####
    make_figures(params)



if __name__ == "__main__":
    main()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        