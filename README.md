# hcswif
Beta version of a python script for running batches of Hall C replay scripts
on ifarm using swif.

Usage:
```
python hcswif.py --spectrometer (HMS|SHMS|COIN) --run <list of runs> --events <number of events> --outfile <output json> --project <project>
```

Generates a file (default name hcswif##########.json) containing JSON data that
describe a swif workflow. The JSON data should be imported with:
```
swif import -workflow foo.json
```

The output is formatted as one long string, but the following command will
display it in a pretty format:
```
python -m json.tool foo.json
```
