#!/bin/bash

# -----------------------------------------------------------------------------
#  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#  !!!     CHANGE ME IF THIS IS NOT WHERE hallc_replay AND hcana LIVE     !!!
#  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
export hcana_dir=/volatile/hallc/comm2017/$USER/hcana
export hallc_replay_dir=/volatile/hallc/comm2017/$USER/hallc_replay
# -----------------------------------------------------------------------------

# Source setup scripts
curdir=`pwd`
cd $hcana_dir
source setup.sh
cd $hallc_replay_dir
source setup.sh
cd $curdir
export PATH=$halllc_replay_dir:$hcana_dir:$PATH
