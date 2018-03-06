# hcswif
Beta version of a python script for running batches of Hall C replay scripts
on ifarm using swif. hcswif generates a file (default name hcswif##########.json)
containing JSON data that describe a swif workflow.

The json output is formatted as one long string, but the following command will
display it in a pretty format:
```
python -m json.tool myswifjob.json
```

# Initial setup
You'll need to modify a few files so that hcswif points to the correct hcana, raw data, etc.

The following is a list of files and variables that you may need to modify:
```
1) hcswif.py
    - out_dir
    - raw_dir
2) setup.sh
    - hcana_dir
    - hallc_replay_dir
    - Version of /site/12gev_physics/production.sh
```

# Usage
```
python hcswif.py --spectrometer (HMS|SHMS|COIN|HMS_COIN|SHMS_COIN) --run <a space-separated list of runs> --events <number of events> --outfile <output json> --replay <hcana replay script> --project <project>
```
You must specify at least a spectrometer and run.

Default number of events is all (i.e. -1).

Default project is c-comm2017.

# Example
```
python hcswif.py --spectrometer SHMS_COIN --run 2296 2297 --outfile myswifjob.json --project c-comm2017
swif import -file myswifjob.json
swif run myswifjob
```
