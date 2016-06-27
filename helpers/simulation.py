import os
import random
import json
#from SimonsPythonHelpers import nestedPrint


def run_simulation(allsimparams ,metaparams ,wetRun=True):
    os.system( 'mkdir -p ' +metaparams.data_path)
    os.chdir(metaparams.data_path)

    parjobfile = open('par_jobs.txt', 'w')


    theCmdString = ""
    theRedirectString = ""
    numParameterSets = len(allsimparams)
    if numParameterSets > 1 or metaparams.numRepetitions > 1:
        theRedirectString = ' 1> stdout.txt 2> stderr.txt'

    for paramsetID in xrange(numParameterSets):
        simparams = allsimparams[paramsetID]
        paramsetFoldername = 'psim'
        shortParamStrings = {}
        for psimParamString in simparams.extendedparams: # make a dict of just the last part of each param string
            if '.' in psimParamString:
                lastDotPosition = psimParamString.rfind('.')
                shortParamStrings[psimParamString[ lastDotPosition +1:]] = psimParamString
            else:
                shortParamStrings[psimParamString] = psimParamString
        for shortParamString in sorted \
                (shortParamStrings.keys()): # sort that dict's keys and create folder name of params in alphabetical order.
            psimParamString = shortParamStrings[shortParamString]
            paramsetFoldername += '_'+ shortParamString + str(simparams.extendedparams[psimParamString])
        simparams.extendedparamFoldername = paramsetFoldername
        os.system('mkdir -p ' + paramsetFoldername)
        os.chdir(paramsetFoldername)

        for repetitionID in xrange(metaparams.numRepetitions):
            repfolder = metaparams.repetitionFoldernames[repetitionID]
            os.system('mkdir -p ' + repfolder)

            simparams.repetitionID = repetitionID
            simparams.neurongroups.inputs.randomseed = int(random.randint(0, 2 ** 30))  # long(time.time())
            paramfile = open(repfolder + '/settings_simulation.json', 'w')
            json.dump(simparams.toDict(), paramfile, sort_keys=True, indent=4, separators=(',', ': '))
            paramfile.close()

            # paramfile = open(metaparams.data_path+'settings_recording.json', 'w')
            # json.dump(oneSimParams.recordings.toDict(), paramfile, sort_keys=True, indent=4, separators=(',', ': '))
            # paramfile.close()

            # if (repetitionID+1 == metaparams.numRepetitions) and (paramsetID+1 == numParameterSets):
            #    theRedirectString = ""

            theCmdString += "( cd " + paramsetFoldername + '/' + repfolder + " ; " + '../../../../' + metaparams.executable_path + metaparams.executable_file + ' --settingsfile ' + os.getcwd() + '/' + repfolder + '/settings_simulation.json ' + theRedirectString + '; cd ../../.. ) &'

            simString = " cd " + paramsetFoldername + '/' + repfolder + " ; " + '../../../../' + metaparams.executable_path + metaparams.executable_file + ' --settingsfile ' + os.getcwd() + '/' + repfolder + '/settings_simulation.json ' + theRedirectString + '; cd ../../..  \n'
            parjobfile.write(simString)

        os.chdir('..')

    theCmdString += "time wait "

    # os.system('time ../'+sim_executable_path+sim_executable_file+' '+' --seed='+str(simparams.neurongroups.inputs.randomseed)+' --simtime='+str(simparams.general.simtime)+' --Npre='+str(simparams.neurongroups.inputs.N)+' ')
    # os.system('time ../'+sim_executable_path+sim_executable_file+' '+'  ')
    # os.system('time ../'+sim_executable_path+sim_executable_file+' --show-settings'+'  ')
    # os.system('time ../'+sim_executable_path+sim_executable_file+' --show-settings --settingsfile /Users/simon/Workspaces/WorkspaceGIT/MyGitHubAccount/auryn/plot/sim_simon1.data/settings_simulation.json '+'  ')
    # os.system('time ../'+sim_executable_path+sim_executable_file+' --show-settings --settingsfile '+os.getcwd()+'/settings_simulation.json '+'  ')
    # os.system('time ../'+sim_executable_path+sim_executable_file+' --settingsfile '+os.getcwd()+'/settings_simulation.json '+'  ')
    # print "The command string is:"
    # print theCmdString

    parjobfile.close()

    if numParameterSets > 1:
        print "Now running sims for " \
              + str(numParameterSets) \
              + " parameter sets with " \
              + str(metaparams.numRepetitions) \
              + " repetitions each (" + str(numParameterSets * metaparams.numRepetitions) \
              + " parallel jobs). Screen output redirected to stdout.txt and stderr.txt to avoid terminal confusion."
    else:
        print "Now running sims for " \
              + str(numParameterSets) \
              + " parameter sets with " \
              + str(metaparams.numRepetitions) \
              + " repetitions each (" \
              + str(numParameterSets * metaparams.numRepetitions) \
              + " parallel jobs). Showing screen output here."

    if wetRun:
        gnuParallelCmdString = "time parallel --bar --joblog " + os.getcwd() + "/joblog.txt :::: par_jobs.txt"
        os.system(gnuParallelCmdString)
        # os.system(theCmdString)
    else:
        print "Skipping sims!"  # dry run

    os.chdir('../..')

    pass


