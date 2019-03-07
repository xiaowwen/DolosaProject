#!/usr/bin/env python3
#
# This program removes contigs given in alist from a fasta
# file. The following arguments are required (in tgeexact same
# order.
# fastq reads. It requires these arguments:
# First argument: List of contigs to be removed
# Second argument: Fasta list of sequences
# Third argument: Output fasta

import sys

if len(sys.argv) < 4:
    print('''############################################################
#                                                          #
# To be employed to removed contigs deemed contamination   #
#                                                          #
# \033[1mcontig_remover.py\033[0m <CONTIG_LIST> <IN_FASTA> <OUT_FASTA>   #
#                                                          #
# This program removes contigs given in a list from a      #
# fasta file. The following arguments are required (in     #
# the exact same order):                                   #
# First argument: list of contigs to be removed            #
# Second argument: fasta list of sequences                 #
# Third argument: output fasta                             #
#                                                          #
############################################################
    ''')
    sys.exit();

# Retrieve reads to be removed from fastq
def get_to_be_removed_contigs(contigs_file):
    list = []
    with open(contigs_file) as file:
        for line in file:
            list.append(line.strip())
    return set(list)

remove_list = get_to_be_removed_contigs(sys.argv[1])

# Input fasta file
in_name = sys.argv[2]
fasta_in = open(in_name,"r")

# Output fasta file
fasta_out = open(sys.argv[3],"w")

# Go through list and identify which contigs to remove 

for line in fasta_in:
    print(line.strip()[1:])
    if line.strip()[1:] in remove_list:
        print("NOT "+line.strip())
        fasta_in.readline()

    else:
        fasta_out.write(line.strip()+"\n")
        fasta_out.write(fasta_in.readline().strip()+"\n")

fasta_in.close()
fasta_out.close()
