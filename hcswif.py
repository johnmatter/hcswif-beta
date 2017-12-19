import os
import sys
import copy
import json
import getpass
import argparse
import datetime

#------------------------------------------------------------------------------
# Preliminary workspace stuff

# Where do you want the output of your analyses?
work_dir = os.path.join('/volatile/hallc/comm2017/', getpass.getuser())
if not os.path.isdir(work_dir):
    raise StandardError('work_dir: ' + work_dir + ' does not exist')

# Where is your raw data?
raw_dir = '/mss/hallc/spring17/raw'
if not os.path.isdir(raw_dir):
    raise StandardError('raw_dir: ' + raw_dir + ' does not exist')

# Where is hcswif?
hcswif_dir = os.path.dirname(os.path.realpath(__file__))

# hcswif_prefix is used as prefix for workflow, job names, filenames, etc.
now = datetime.datetime.now()
datestr = now.strftime("%Y%m%d%H%M")
hcswif_prefix = 'hcswif' + datestr 

#------------------------------------------------------------------------------
# Parse command line arguments
parser = argparse.ArgumentParser(usage='python hcswif.py (hms | shms | coin)' +
                                       '--run <list of runs>' +
                                       '--events <number of events>' +
                                       '--outfile <output json>')

# Add arguments
parser.add_argument('spectrometer', nargs=1, 
                    help='spectrometer to analyze (HMS, SHMS, COIN)')
parser.add_argument('--run', nargs='+', dest='run', 
                    help='a space-separated list of run number(s)')
parser.add_argument('--events', nargs=1, dest='events',
                    help='number of events to analyze (default=50k)')
parser.add_argument('--outfile', nargs=1, dest='outfile', 
                    help='name of output json file')
parser.add_argument('--project', nargs=1, dest='project', 
                    help='name of project')

# Parse arguments
parsed_args = parser.parse_args()

# Check validity of arguments, then assign 
# Spectrometer
spectrometer = parsed_args.spectrometer[0]
if spectrometer.upper() not in ['HMS','SHMS','COIN']:
    raise ValueError('Spectrometer must be HMS, SHMS, or COIN')

# Number of events
if parsed_args.events==None:
    evts = 50000
else:
    evts = parsed_args.events[0]

# Run(s)
if parsed_args.run==None:
    raise StandardError('Must specify run(s) to process')
else:
    runs = parsed_args.run

# Outfile
if parsed_args.outfile==None:
    outfile = hcswif_prefix + '.json'
    outfile = os.path.join(work_dir, outfile)
else:
    outfile = parsed_args.outfile[0]

# Project
if parsed_args.project==None:
    raise StandardError('Must specify a project')
else:
    project = parsed_args.project[0]

#------------------------------------------------------------------------------
# Create JSON

# Initialize workflow JSON data
workflow = {}
workflow['name'] = hcswif_prefix

# Choose correct batch for config (e.g. hcswif_shms.sh)
batch = os.path.join(hcswif_dir, 'hcswif_' + spectrometer.lower() + '.sh')

# Load template json for one job, then create list of jobs
with open('job_template.json', 'r') as f:
    job_template = json.load(f)

# Initialize dictionary whose key is the run number, value is a run's JSON data
jobs = {}
for run in runs:
    # Initialize JSON
    job = copy.deepcopy(job_template) 

    # Assume coda name e.g. shms_all_01634
    coda_stem = spectrometer.lower() + '_all_' + str(run).zfill(5)
    coda = os.path.join(raw_dir, coda_stem + '.dat')

    # Check if raw data file exist
    if not os.path.isfile(coda):
        raise StandardError('RAW DATA: ' + coda + ' does not exist')

    # Fill various fields; some are optional!
    job['project'] = project
    job['email'] = getpass.getuser() + '@jlab.org'
    job['name'] = workflow['name'] + '_' + coda_stem

    job['stdout'] = os.path.join(work_dir, job['name'] + '.out')
    job['stderr'] = os.path.join(work_dir, job['name'] + '.err')

    job['command'] = " ".join([batch, str(run), str(evts)])

    job['track'] = 'analysis'
    job['shell'] = '/bin/bash'
    job['os'] = 'centos7'
    job['diskBytes'] = 10000000000
    job['ramBytes'] = 8000000000
    job['cpuCores'] = 8
    job['timeSecs'] = 14400


    job['input'][0]['local'] = os.path.basename(coda)
    job['input'][0]['remote'] = coda
    job['output'][0]['local'] = 'result'
    job['output'][0]['remote'] = os.path.join(work_dir, job['name'] + '.root')
    job['output'][1]['local'] = 'meta'
    job['output'][1]['remote'] = os.path.join(work_dir, job['name'] + '.meta')


    jobs[run] = copy.deepcopy(job)

# Put jobs' JSON data into the workflow
workflow['jobs'] = jobs.values()

#------------------------------------------------------------------------------
# Export JSON
with open(outfile, 'w') as f:
    json.dump(workflow, f)

print 'Wrote: ' + outfile
