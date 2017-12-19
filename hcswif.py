import os
import sys
import copy
import json
import getpass
import argparse
import datetime

#----------------
# Setup argparser
parser = argparse.ArgumentParser(usage='%(prog)s SPECTROMETER --run R1 R2 ...')

parser.add_argument('spectrometer', nargs=1, 
                    help='spectrometer to analyze (HMS, SHMS, COIN)')
parser.add_argument('--run', nargs='+', dest='run', 
                    help='a space-separated list of run number(s)')

parsed_args = parser.parse_args()

# datestr is used to name files, jobs, etc.
now = datetime.datetime.now()
datestr = now.strftime("%Y%m%d%H%M")

# workdir should be a user's or an experiment's
work_dir = os.path.join('/volatile/hallc/comm2017/', getpass.getuser())
work_dir = '/Users/matter/jlab/hcswif'

# if work_dir doesn't exist, exit and warn user
if not os.path.isdir(work_dir):
    raise StandardError('work_dir: ' + work_dir + ' does not exist')

#----------------
# Check if spectrometer is valid
spectrometer = parsed_args.spectrometer[0]
if spectrometer.upper() not in ['HMS','SHMS','COIN']:
    raise ValueError('Spectrometer must be HMS, SHMS, or COIN')

#----------------
# hcswifdate is used as prefix for workflow, job names, filenames, etc.
hcswifdate = 'hcswif' + datestr 

#----------------
# Initialize workflow JSON data
workflow = {}
workflow['name'] = hcswifdate

#----------------
# Choose correct batch for config (e.g. hcswif_shms.sh)
batch = 'hcswif_' + spectrometer.lower() + '.sh'

#----------------
# Load template json for one job, then create list of jobs
with open('job_template.json', 'r') as f:
    job_template = json.load(f)


# Initialize dictionary whose key is the run number, and value is a run's JSON data
jobs = {}
runs = parsed_args.run  # runs specified by user
for run in runs:
    # Initialize
    job = copy.deepcopy(job_template) 

    # e.g. shms_all_01634
    coda_stem = spectrometer.lower() + '_all_' + str(run).zfill(5)
    coda = os.path.join('/mss/hallc/spring17/raw', coda_stem + '.dat')

    job['project'] = '?????????' # scicomp website doesn't currently have a list
    job['email'] = getpass.getuser() + '@jlab.org'
    job['name'] = workflow['name'] + '_' + coda_stem

    job['stdout'] = os.path.join(work_dir, job['name'] + '.out')
    job['stderr'] = os.path.join(work_dir, job['name'] + '.err')

    job['command'] = batch

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

# Puts jobs' JSON data into the workflow
workflow['jobs'] = jobs.values()

#----------------
# Export JSON
with open(workflow['name'] + '.json', 'w') as f:
    json.dump(workflow, f)
