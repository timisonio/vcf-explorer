#!/usr/bin/python

import argparse
import hashlib
import sys
import os
import gzip

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--checksum", action="store_true")
    args = parser.parse_args()

    # Use file modified time, basically instantaneous
    input_hash = str(os.stat(args.input).st_mtime) + '\n' + str(os.stat(args.input).st_size)
    
    if args.checksum == True:
        # Compute hash of input file, slow and memory intensive
        sha = hashlib.sha1()
        sha.update(open(args.input, 'rb').read())
        input_hash = input_hash + '\n' + sha.hexdigest()
    else:
        input_hash = input_hash + '\n' + '0'
        

    outputname = args.input + ".vcfe"

    try:
        with open(outputname, 'r') as output:
            # read in old hash
            output_hash = []
            for output_line in output:
                if output_line.startswith("begin"):
                    break
                output_hash.append(output_line.strip())
            # If hash was same as before, no need to continue
            if output_hash == input_hash.split('\n'):
                print("VCF file not changed. No need to re-create offsets.")
                sys.exit()
            # File has been changed
            else:
                print("VCF file changed since last offset creation. Re-creating offsets.")
    except EnvironmentError:
        # File not present
        print("VCFE file not found, creating offsets.")

    with open(outputname, 'w') as output:
        # Print input file's hash to output file
        print(input_hash, file=output)
        print("begin offsets", file=output)
        
        with gzip.open(args.input, 'r') as infile:
            # consume lines until actual content
            infile_line = infile.readline()
            while not infile_line.startswith(b"#CHROM"):
                infile_line = infile.readline()

            offsets = {}

            for infile_line in infile:
                # vcf format has chromosome as the first column, then a tab
                infile_line_chromosome = infile_line.split(b'\t')[0]
                
                if infile_line_chromosome not in offsets:
                    # get current position in file
                    offset = infile.tell()
                    
                    # store into dictionary
                    offsets[infile_line_chromosome] = offset
                    
                    # progress update
                    print("Adding offset", offset, "for chromosome", infile_line_chromosome)
                    
                    # print to vcfe file
                    print(infile_line_chromosome, offset, sep='\t', file=output)
                    output.flush()
    
