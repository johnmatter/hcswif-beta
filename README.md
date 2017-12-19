# hcswif
Beta version of a python script for running batches of Hall C replay scripts
on ifarm using swif.

Usage:
```
python hcswif.py {hms | shms | coin} --run <list of runs>
```

Generates a file named hcswif#######.json that can be imported with:
```
swif import -workflow foo.json
```

The output is formatted as one long string, but the following command will
display it in a pretty format:
```
python -m json.tool foo.json
```
