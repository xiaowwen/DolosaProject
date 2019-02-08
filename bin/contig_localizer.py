#!/usr/bin/env python3

# This program identifies which contigs have a coverage lower
# than a given value or map to a genus other than the one spe-
# cified in step 1. 
# first argument: parsed blast result from step 1
# second argument: minimum coverage
# third argument: out file  

import sys

if len(sys.argv) < 4:
    print('''################################################################
#                                                              #
# STEP 2 of decontamination pipeline                           #
#                                                              #
# \033[1mcontig_localizer.py\033[0m <PARSED_BLAST> <MIN_COVERAGE> <OUT_FILE> #
#                                                              #
# This program identifies which contigs have a coverage lower  #
# than a given value or map to a genus other than the one spe- #
# cified in step 1. There are three required arguments (in the #
# exact same order):                                           #
# First argument: parsed blast result from step 1              #
# Second argument: minimum coverage                            #
# Third argument: out file                                     #
#                                                              #
################################################################
    ''')
    sys.exit();

frame = []
in_file = sys.argv[1]
with open(in_file) as file:
    next(file)
    for line in file:
        info = line.strip().split(",")
        contig = info[0]
        coverage = info[2]
        circle = info[3]

        if float(coverage) < 10:
            frame.append(contig)
        elif circle == "red":
            frame.append(contig)
     
out_file = open(sys.argv[2], "w")
for item in frame:
    out_file.write(item+"\n")
out_file.close()