#!/usr/bin/python

import argparse
import hashlib
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=argparse.FileType('r'))
    args = parser.parse_args()

    # Compute hash of input file
    sha = hashlib.sha256()
    for line in args.input:
        sha.update(bytes(line, 'utf-8'))

    input_hash = sha.hexdigest()
    outputname = args.input.name + ".vcfe"

    try:
        with open(outputname, 'r') as output:
            # If hash was same as before, no need to continue
            if output.readline().strip() == input_hash:
                print("No need to redo offsets; file not changed.")
                sys.exit()
            # File has been changed
            else:
                print("File changed since last offset creation. Re-creating offsets.")
    except EnvironmentError:
        # File not present
        print("File not found, creating offsets.")

    with open(args.input.name + '.vcfe', 'w') as output:
        print(sha.hexdigest(), file=output)
    
