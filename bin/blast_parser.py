#!/usr/bin/env python3

#This program checks if contig blasts to genus of interest.
# First argument: blast results
# Second argument: assembly metrics
# Third argument: genus of interest
# Fourth argument: out file

import sys

if len(sys.argv) < 5:
    print('''#######################################################################
#                                                          #
# STEP 1 of decontamination pipeline                       #
#                                                          #
# \033[1mblast_parser.py\033[0m <BLAST_RESULT> <ASSEMBLY_METRICS> <GENUS> <OUT_FILE> #
#                                                                      #
# This program checks whether each contig from an assembly has a blast #
# hit in a genus of interest. If the contig has a blast hit from the   #
# genus of interest, the contig is given a monochromatic colour. Other-#
# wise, the contig is assigned a red colour. The following four argum- #
# ents are required (in the exact same order):                         #
# First argument: blast results                                        #
# Second argument: assembly metrics                                    #
# Third argument: genus of interest                                    #
# Fourth argument: out file                                            #
#                                                                      #
########################################################################
    ''')
    sys.exit();

# Parse Taxonomic information to return only genus.
def get_genus(name):
    return(name.split(" ")[0])
    
# Parse blast results to obtain only the Taxonomic information 
# of each blast hit.
def get_blast(blast_file):
    frame = []
    with open(blast_file) as file:
        for line in file:
            data = line.strip().split(",")
            contig = data[0]
            genus = get_genus(data[13])
            frame.append((contig, genus))
    return frame

# Retrieve information from the assembly metrics tsv file
def get_csv(csv_file):
    frame = []
    with open(csv_file) as file:
        for line in file:
            item_list = line.strip().split("\t")
            frame.append(item_list)
    return frame
        
#final out
out_name = sys.argv[4]
file_out = open(out_name, "w")
        
# File including blast result
blast = get_blast(sys.argv[1])

# File with assembly metrics
csv = get_csv(sys.argv[2])

# Loop through assembly metrics file to see if contig has genus of interest hit 
for item in csv:
    if item[0] != 'ContigId':
        temp_list = []
        contig = item[0]
        for hit_contig, hit_genus in blast:
            if hit_contig == contig:
                temp_list.append(hit_genus)
        if len(temp_list) is 0:
            circle, fill = "black", "grey"
        else:
            # Genus to search for
            if sys.argv[3] in temp_list:
                circle, fill = "black", "grey"
            else:
                circle, fill = "red", "pink"

        file_out.write("{},{},{},{},{}\n".format(item[0],item[1],item[2],circle,fill))
    else:
        file_out.write("ContigId,ContigLength,ContigCoverage,circle,fill\n")
                
file_out.close()
                
