#!/usr/bin/env python3
#
# This program removes a list of reads from paired
# fastq reads. It requires these arguments:
# First argument: List of reads to be removed
# Second argument: Fastq read one
# Third argument: Fastq read two
# Fourth argument: out fastq read one
# Fifth argument: out fastq read two

import sys

if len(sys.argv) < 6:
    print('''#####################################################################
#                                                                   #
# STEP 4 of decontamination pipeline                                #
#                                                                   #
# \033[1mread_remover.py\033[0m <READ_LIST> <FQ_ONE> <FQ_TWO> <OUT_ONE> <OUT_TWO> #
#                                                                   #
# This program removes reads given in a list from paired fastq      #
# files. The following arguments are required (in the exact same    #
# order):                                                           #
# First argument: list of reads to be removed                       #
# Second argument: read one of input paired fastq                   #
# Third argument: read two of input paired fastq                    #
# Fourth argument: read one of output fastq                         #
# Fifth argument: read two of output fastq                          #
#                                                                   #
#####################################################################
    ''')
    sys.exit();

# Retrieve reads to be removed from fastq
def get_to_be_removed_reads(reads_file):
    list = []
    with open(reads_file) as file:
        for line in file:
            list.append(line.strip())
    return list

remove_list = get_to_be_removed_reads(sys.argv[1])

# Input read one and read two
one_name = sys.argv[2]
two_name = sys.argv[3]

one = open(one_name,"r")
two = open(two_name,"r")

# Output read one and read two
one_out = open(sys.argv[4],"w")
two_out = open(sys.argv[5],"w")

# Go through reads anf identify which reads to remove 
for line in one:
    if line.strip()[1:-2] in remove_list:
        print("NOT "+line.strip())
        one.readline()
        one.readline()       
        one.readline()
        
        print("NOT "+two.readline().strip())        
        two.readline()
        two.readline()
        two.readline()
    else:
        one_out.write(line.strip()+"\n")
        one_out.write(one.readline().strip()+"\n")
        one_out.write(one.readline().strip()+"\n")
        one_out.write(one.readline().strip()+"\n")
                
        two_out.write(two.readline().strip()+"\n")
        two_out.write(two.readline().strip()+"\n")
        two_out.write(two.readline().strip()+"\n")
        two_out.write(two.readline().strip()+"\n")

one.close()
two.close()
one_out.close()
two_out.close()
