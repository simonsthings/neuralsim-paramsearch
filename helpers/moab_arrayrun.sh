#!/bin/bash
# This script selects a set of lines out of a given $JOBLISTFILE and executes them in turn.
# To view the available environment variables, do something like this here: export > /home/fr/fr_fr/fr_sv1021/playground/moab_sim_tests/job_environment1_${PBS_JOBID}_$MOAB_JOBARRAYINDEX.txt
#
# Moab special parameters (these are actually used, despite the comment natur of the lines below!)
#MSUB -l nodes=1:ppn=1
#MSUB -l walltime=3:00:00
#MSUB -m bea
#MSUB -M simon.vogt@blbt.uni-freiburg.de

# $JOBLISTFILE will usually be either "par_jobs.txt" or "par_jobs_repeatmissing.txt" and is passed to msub via the -v option.
THEJOBLIST="${PBS_O_WORKDIR}/${JOBLISTFILE}"
WC_OUT=$(wc -l ${THEJOBLIST})
TOTAL_PSIMS=${WC_OUT% *}

#total number of jobs: MOAB_JOBARRAYRANGE
PSIMS_PER_JOB=$((TOTAL_PSIMS/MOAB_JOBARRAYRANGE))
# get ceiling of previous division:
if (( (PSIMS_PER_JOB*MOAB_JOBARRAYRANGE) < TOTAL_PSIMS )); then
  PSIMS_PER_JOB=$((PSIMS_PER_JOB+1)) ;
fi

#JOB_NUM=$MOAB_JOBARRAYINDEX
#echo "Now running psim ${PSIM_NUM}!"

# run (possibly) more than one psim within this moab-job:
for ((PSIM_NUM_WITHIN_JOB=1;PSIM_NUM_WITHIN_JOB<=PSIMS_PER_JOB;PSIM_NUM_WITHIN_JOB++))
do
  # (JOB_NUM-1) * PSIMS_PER_JOB + PSIM_NUM_WITHIN_JOB
  PSIM_NUM=$(( (MOAB_JOBARRAYINDEX-1) * PSIMS_PER_JOB + PSIM_NUM_WITHIN_JOB    ))

  # the last job may not have all PSIMS_PER_JOB to run:
  if ((PSIM_NUM <= TOTAL_PSIMS)); then
    PSIM_CMD=$(sed "${PSIM_NUM}q;d" ${THEJOBLIST})
    #echo "The commands to be executed are:"
    #echo $PSIM_CMD
    echo $PSIM_NUM >> ${PBS_O_WORKDIR}/psims_started.txt
    eval $PSIM_CMD
    echo $PSIM_NUM >> ${PBS_O_WORKDIR}/psims_finished.txt
  fi
done






