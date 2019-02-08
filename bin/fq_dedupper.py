#!/usr/bin/env python3
#
# Removes duplicates from a set of fastq paired end reads.
# 
# Requires two fastq files and a reference for mapping the
# fastq reads to. Environment variables BWA, SAMTOOLS, and
# PICARD must be set to the executables for bwa, samtools, 
# and picard, respectively.
#
# Step 1: Map reads to complete genome reference with bwa
# Step 2: Sort reads from the sam mapping with samtools
# Step 3: Remove duplicates with picard 
# Step 3: Convert bam to fastq files with picard

def get_base_name(in_name):
    index = in_name.rfind("_")
    return in_name[:index]

def test_file(file_name):
    if not os.path.isfile(file_name):
        print("usage:           fq_dedupper.py "+use[19:])
        print("fq_dedupper.py: error: '"+file_name+"' does not exist")
        sys.exit(1)

def get_env_var(var_label, use):
  try:
    value = os.environ[var_label]
    test_file(value)
  except KeyError:
    print("usage:           fq_dedupper.py "+use[19:])
    print("fq_dedupper.py: error: environment variable '"+var_label+"' has not been set.")
    print("                       (e.g 'export "+var_label+"=/path/to/"+var_label.lower()+"')")
    sys.exit(1)
  return value


import os
import sys
import argparse


desc = """\n\033[1mfq_dedupper\033[0m       this program is intended to remove duplicated reads from a set
                  of fastq paired end reads. It implements the MarkDuplicates 
                  program from picard. The pipeline takes the following steps:
                  1. Reads are mapped to a reference
                  2. The alignment is sorted
                  3. Removal duplicate reads
                  4. Printing results as fastq

                  This program requires bwa (v. 0.7.17), samtools(v. 1.8),
                  and picard (v. 2.18.4), which need to be set in the 
                  environment variables BWA, SAMTOOLS, and PICARD, respectively."""

epi = "\nquestions:        julio.diaz@mail.utoronto.ca"
use = """           %(prog)s [-h] [-o1 FQ_ONE_OUT] [-o2 FQ_TWO_OUT] \\
                                 [-b] [-ob BASH_OUT] \\
                                 reference fastq_one fastq_two"""

BWA_BINARY = get_env_var("BWA", use)
SAMTOOLS_BINARY = get_env_var("SAMTOOLS", use)
PICARD_JAR = get_env_var("PICARD", use)

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, 
    description=desc, epilog=epi, usage=use)
parser.add_argument("-o1", help="name for resulting read one fastq", 
    metavar="FQ_ONE_OUT", type=argparse.FileType('w'))
parser.add_argument("-o2", help="name for resulting read two fastq", 
    metavar="FQ_TWO_OUT", type=argparse.FileType('w'))
parser.add_argument("-b","--bash", help="prints the pipeline to a bash script",
    action="store_true")
parser.add_argument("-ob", help="name for bash script file (disergarded if -b is not called)",
    metavar="BASH_OUT", type=argparse.FileType('w'))
parser.add_argument("reference", help="indexed reference file", 
    type=argparse.FileType('r'))
parser.add_argument("fastq_one", help="input read one fastq",
    type=argparse.FileType('r'))
parser.add_argument("fastq_two", help="input read two fastq",
    type=argparse.FileType('r'))
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()


#BWA_BINARY = "/Users/juliofdiaz/Software/bwa-0.7.17/bwa"
#SAMTOOLS_BINARY = "/Users/juliofdiaz/Software/samtools-1.8/samtools"
#PICARD_JAR = "/Users/juliofdiaz/Software/picard.jar"

# get name of rerference file
reference_file = os.path.realpath(args.reference.name)

# get name of input fastq files
read_one = os.path.realpath(args.fastq_one.name)
args.fastq_one.close()
read_two = os.path.realpath(args.fastq_two.name)
args.fastq_two.close()

# get base name for default name 
base_name = get_base_name(read_one)

# names of intermediate steps
out_sam = "{}.ddp.sam".format(base_name)
out_bam = "{}.dd0.bam".format(base_name)
dedup_bam = "{}.ddp.bam".format(base_name)
dedup_metrics = "{}.ddp.mtcs".format(base_name)
    
# if out file is not given, give the canonical names
if args.o1:
    out_read_one = os.path.realpath(args.o1.name)
    args.o1.close()
    os.remove(out_read_one)
else:
    out_read_one = "{}_1.ddp.fq".format(base_name)

if args.o2:
    out_read_two = os.path.realpath(args.o2.name)
    args.o2.close()
    os.remove(out_read_two)
else:
    out_read_two = "{}_2.ddp.fq".format(base_name)

# if out bash file is not given, give the cannonical one
if args.ob:
    out_file = os.path.realpath(args.ob.name)
    args.ob.close()
    os.remove(out_file)
else:
    out_file = "{}.ddp.sh".format(base_name)
    
# bash command lines
sammer = "{} mem {} {} {} > {}\n".format(BWA_BINARY, reference_file, read_one, read_two, out_sam)
bammer = "{} sort -o {} -O BAM {}\n".format(SAMTOOLS_BINARY, out_bam, out_sam)
dedupper = "java -jar {} MarkDuplicates I={} O={} M={} TAG_DUPLICATE_SET_MEMBERS=true TAGGING_POLICY=All REMOVE_SEQUENCING_DUPLICATES=true\n".format(PICARD_JAR, out_bam, dedup_bam, dedup_metrics)
fastqer = "java -jar {} SamToFastq I={} FASTQ={} SECOND_END_FASTQ={}\n".format(PICARD_JAR, dedup_bam, out_read_one, out_read_two)

# print to bash file to be run later
if args.bash:
    file = open(out_file, "w")
    file.write("#!/bin/bash\n\n")    
    file.write(sammer+"\n")
    file.write(bammer+"\n")
    file.write(dedupper+"\n")
    file.write(fastqer+"\n")
    file.close()
# or execute now
else:
    print("# 1. Mapping reads to reference")
    os.system(sammer)
    print("# 2. Sorting reads")
    os.system(bammer)
    print("# 3. Removing duplicates")
    os.system(dedupper)
    print("# 4. Printing fastq files")
    os.system(fastqer)


