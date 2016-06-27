import os
import numpy as np
import dotmap

from helpers.parameters import flattenExtendParamsets, crossAllParamsets
from helpers.simulation import run_simulation

from figures.overview import make_overview_figures
from figures.repetitiondetail import make_singlerun_figures
from figures.repetitionsummary import make_repetitionsummary_figures


def define_extended_simulation_parameters(metaparams,baseParams):
    """
    The helpers of baseParams that should be re-run with a list of settings each.
    Node paths of extendedParams have to match those in baseParams.
    """

    extendedParams = dotmap.DotMap()
    extendedParams.neurongroups.outputs.userecovery = [True,False]
    extendedParams.neurongroups.inputs.rate = [ 10 , 15 ] # Hz
    #extendedParams.neurongroups.outputs.projMult = np.r_[0.2:4.2:0.2]
    #extendedParams.neurongroups.outputs.projMult = np.r_[0.2:2.2:0.2]
    #extendedParams.neurongroups.outputs.projMult = np.r_[2.2:4.2:0.2]
    extendedParams.neurongroups.outputs.projMult = [ 1.0 , 1.5 , 1.8 ]

    extendedParams.connectionsets.con1.stdprule.learningrate = 1/32.0 * np.array([1/1.0 , 2.0]) # eta in Auryn
    #extendedParams.connectionsets.con1.stdprule.learningrate = 1/32.0 * np.r_[0.2:4.2:0.2]

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
    detailedtracking = False
    
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
    # projMult ; input rate ; learningrate ; (STDP shape) ; (use_recovery) ; (dt) ; ...


    ## without recovery: best is projMult=0.8 with learningrate * 2
    # projMult = 0.5 * ms/dt; // without recovery: learning works (*2), but then the neuron hardly ever manages to produce a spike!
    # projMult = 0.8 * ms/dt; // 8.0; without recov: one-spike responses already at lr/1 ! But 2/6 do not learn within 400s. /2 seems to work more often than not, but always only after 400s. *2 surprisingly also works nicely! surprisingly well! best!  *4 doesn't work. *3 hardly ever works.
    # projMult = 1.0 * ms/dt; // 8.0;  // without recovery: works for lr 1 with double spike. lr/2 looses 2nd spike :) (but takes longer than 400s to start sometimes, on /3 is takes more than 1600s often.)
    # projMult = 1.5 * ms/dt; // 8.0;  // without recovery: only works for learningrate between /1 and /3

    ## with recovery:
    # projMult = 1.5 * ms/dt; // 8.0;  // with recovery! works with learningrate /4 to *10 and beyond.
    # projMult = 50.5 * ms/dt; // 8.0;
    
    
    simparams.connectionsets.con1.presynaptic = "inputs"
    simparams.connectionsets.con1.postsynaptic = "outputs"
    simparams.connectionsets.con1.initialweight = 0.85
    
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
    recordingparams.detailedtracking = detailedtracking
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
    metaparams.numRepetitions = 8
    for repetitionID in xrange(metaparams.numRepetitions):
        metaparams.repetitionFoldernames[repetitionID] = 'repetition_'+str(repetitionID+1)
    return metaparams


def make_figures(allsimparams ,metaparams):

    os.system( 'mkdir -p ' +metaparams.figures_path)

    make_overview_figures(allsimparams ,metaparams)

    if allsimparams[0].recordings.detailedtracking:
        make_repetitionsummary_figures(allsimparams ,metaparams)

        # if metaparams.numRepetitions < 5:
        make_singlerun_figures(allsimparams ,metaparams)


def main():
    
    #### Define meta settings: executable, etc... ####
    metaparams = define_meta_parameters()

    ##### Define simulation settings: ####
    baseParams = define_base_simulation_parameters(metaparams)
    extendedParams = define_extended_simulation_parameters(metaparams,baseParams)

    stringIndexedParamsLists = flattenExtendParamsets(metaparams, baseParams, extendedParams)
    #nestedPrint(allsimparams)
    #nestedPrint(stringIndexedParamsLists)
    allsimparams = crossAllParamsets(metaparams, baseParams, stringIndexedParamsLists)
    #nestedPrint(allsimparams)

    #for repetitionID in xrange(metaparams.numRepetitions):
    #    oneSimParams = define_base_simulation_parameters(metaparams)
    #    allsimparams.append(oneSimParams)
    #nestedPrint(allsimparams)
        
    ##### Run simulation(s) #####
    run_simulation(allsimparams, metaparams, True)
    #print (allsimparams[0].extendedparamFoldername)


    ##### Plot results #####
    make_figures(allsimparams,metaparams)



if __name__ == "__main__":
    main()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        