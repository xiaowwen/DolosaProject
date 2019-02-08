#!/usr/bin/env python3
#
# Given a list of contigs and a sam-formatted mapping file. This 
# script returns a list of the sequencing reads that mapped to the
# contigs in the list

# First argument (contig_list): list of contigs to be removed
# Secong argument (file_name): mapping in SAM format
# Third argument (out_file): name of out file
#
import sys

if len(sys.argv) < 4:
    print('''############################################################
#                                                          #
# STEP 3 of decontamination pipeline                       #
#                                                          #
# \033[1mread_localizer.py\033[0m <CONTIG_LIST> <SAM_MAPPING> <OUT_FILE> #
#                                                          #
# This program identifies the reads which map to contigs   #
# listed in a text file. The following arguments are       #
# required (in the exact same order):                      #
# First argument: list of contigs to be removed            #
# Second argument: reads mapped to contigs in SAM format   #
# Third argument: out file                                 #
#                                                          #
############################################################
    ''')
    sys.exit();

# This function retrieves the contigs in the list file.
def get_to_be_filtered_contigs(contig_file):
    list = []

    with open(contig_file) as file:
        for line in file:
            info = line.strip()
            list.append(info)
    print(list)
    return list

# Get contigs from list
filter_list = get_to_be_filtered_contigs(sys.argv[1])
# Alignment in sam format        
file_name = sys.argv[2]

# Go through sam file and if the read maps to listed contigs, 
# add read id to output list. 
list = []
with open(file_name) as file:
    for line in file:
        if line[0] != '@':
            info = line.strip().split("\t")
            if info[2] in filter_list:
                if info[0] not in list:
                    list.append(info[0])

# Print reads mapping to contigs to out file
out_file = open(sys.argv[3],"w")          
for item in list:
    out_file.write(item+"\n")
out_file.close()
