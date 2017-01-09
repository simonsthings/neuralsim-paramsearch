#!/bin/bash

#export > /home/fr/fr_fr/fr_sv1021/playground/moab_sim_tests/job_environment1_${PBS_JOBID}_$MOAB_JOBARRAYINDEX.txt
#echo "The current directory is: $PWD"

PSIM_NUM=$MOAB_JOBARRAYINDEX
#echo "Now running psim ${PSIM_NUM}!"

PSIM_CMD=$(sed "${PSIM_NUM}q;d" ${PBS_O_WORKDIR}/par_jobs.txt)
#echo "The commands to be executed are:"
#echo $PSIM_CMD
eval $PSIM_CMD



