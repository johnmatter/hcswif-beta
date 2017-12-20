#!/bin/bash
ARGC=$#
if [[ $ARGC -ne 2 ]]; then
    echo Usage: hcswif_shms.sh RUN EVENTS
    exit 1
fi;
run=$1
evt=$2

# Setup environment
hcswif_dir=$(dirname $(readlink -f $0))
source $hcswif_dir/setup.sh

# Check environment
# Not sure how best to do this. How do we make sure hcana is in the path?
if [ -z "$(which hcana)" ]; then
    echo Environment not set up! Please edit $hcswif_dir/setup.sh appropriately
    exit 1
fi

# Run analysis
# For now this just runs the production script
cd $hallc_replay_dir
hcana "SCRIPTS/SHMS/PRODUCTION/replay_production_shms.C($run,$evt)"
