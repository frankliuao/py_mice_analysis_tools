# coding = ascii
"""Convert a G4Beamline BL track file (gbeam file) to a json string.

In cases where people like json libraries, use this to convert a gbeam to 
json.

Needs json and numpy modules installed
"""
import sys
import os

import numpy as np
import json


def gbeam2json(in_beam, random_seed=1):
    """Convert gbeam to json string.
    
    :param in_beam: input gbeam;
    :param random_seed: random number seed for all the particles.
        Default=1
    """
    mc_events = []
    gbeam_in = np.copy(in_beam)
    for ii_event in range(gbeam_in.shape[0]):
        mom_ii = np.array([gbeam_in[ii_event, 3], 
                           gbeam_in[ii_event, 4], 
                           gbeam_in[ii_event, 5]])
        mom_tot = np.sqrt(mom_ii[0] ** 2 + mom_ii[1] ** 2 + mom_ii[2] ** 2)
        mc_events.append({"primary": 
            {"random_seed":random_seed,
             "energy":np.sqrt(105.67 ** 2 + mom_tot ** 2), 
             "particle_id":gbeam_in[ii_event, 7], 
             "time":gbeam_in[ii_event, 6], 
             "position":{"x":gbeam_in[ii_event, 0], 
                         "y":gbeam_in[ii_event, 1], 
                         "z":gbeam_in[ii_event, 2]}, 
             "spin":{"x":0, "y":0, "z":0},
             "momentum":{"x":gbeam_in[ii_event, 3],
                         "y":gbeam_in[ii_event, 4], 
                         "z":gbeam_in[ii_event, 5]}}})

    json_lib = {"mc_events": mc_events,
                "spill_number": 1,
                "run_number": 0,
                "daq_event_type": "physics_event",
                "maus_event_type": "Spill"}

    return json.dumps(json_lib)


def main():
    try:
        gbeam_in = np.loadtxt(sys.argv[1])
    except Exception as e:
        print e
        print "---Error: Not able to read the input gbeam file!---"
        sys.exit()
    try:
        random_seed = int(sys.argv[2])
    except Exception as e:
        print e
        print "---Warning: not able to use the second argument as the " + \
              "random number seed, using default value 1"
        random_seed = 1
    json_str = gbeam2json(gbeam_in, random_seed)
    dirname, basename = os.path.split(os.path.abspath(sys.argv[1]))
    filename, ext = os.path.splitext(basename)
    output_path = os.path.join(dirname, filename + ".json")
    outfile = open(output_path, "w")
    outfile.write(json_str)
    outfile.close()


if __name__ == "__main__":
    main()
