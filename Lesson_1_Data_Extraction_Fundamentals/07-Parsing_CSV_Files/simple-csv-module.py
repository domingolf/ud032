import os
import pprint
import csv

DATADIR = ""
DATAFILE = "beatles-diskography.csv"

def parse_csv(datafile):
    data = []
    n = 0

    # Open the file in binary mode (b) and read only (r)
    with open(datafile, "rb") as sd:
        # DictReader class of csv module is used to load the contents of a CSV file into dictionaries.
        # DictReader class assumes that the first row is a header row. The FIELD NAMES are taken from the
        # header row. The FIELD VALUES are taken from the others lines of the file
        r = csv.DictReader(sd)
        for line in r:
            data.append(line)
    return data

def test():
    datafile = os.path.join(DATADIR, DATAFILE)
    d = parse_csv(datafile)

    pprint.pprint(d)

test()