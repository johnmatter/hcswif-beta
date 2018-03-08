# hcswif
hcswif is a python script for generating JSON files that describe a swif workflow to be run on JLab's ifarm

The json output is formatted as one long string, but the following command will
display it in a pretty format:
```
python -m json.tool myswifjob.json
```

Visit these links for more details on swif
https://hallcweb.jlab.org/DocDB/0008/000871/001/SWIF%20Intro.pdf
https://scicomp.jlab.org/docs/swif

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
hcswif is designed to be run with python 3, not python 2
```
./hcswif.py --spectrometer (HMS|SHMS|COIN|HMS_COIN|SHMS_COIN) --run <a space-separated list of runs> --events <number of events> --outfile <output json> --replay <hcana replay script> --project <project>
```
You must specify at least a spectrometer and run.

Default number of events is all (i.e. -1).

# Example
```
./hcswif.py --spectrometer SHMS_COIN --run 2296 2297 --outfile myswifjob.json --project c-comm2017
swif import -file myswifjob.json
swif run myswifjob
```
