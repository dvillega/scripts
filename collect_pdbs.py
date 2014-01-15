#!/usr/bin/env python
"""
Python script to automate downloading pdb files from list received from fludb.org
Devin Villegas
2014/01/02

Input file is tab delimited
PDBid  Description Strain Subtype
Will put downloaded pdbs in <cwd>/subtype/strain/pdbs

Depends on the getentry script from ProtCAD
"""
import csv
import os
import argparse
import re

def which(program):
    """
    Checks for program existence - in python 3.3 we could use shutil.which() instead
    pulled from stackoverflow
    http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def is_valid_file(parser,arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" %arg)
    else:
        return open(arg,'rU')

if which('getentry') is None:
    print("Error: getentry protCAD script is missing")
    exit(1)

parser = argparse.ArgumentParser(description='Download list of pdbs from fludb output')
# Require file is valid - TODO: Add formatting check
parser.add_argument('pdblist',type=lambda x: is_valid_file(parser,x),metavar="FILE",help='Excel file of pdbs to download - fludb output')
args = parser.parse_args()

dict_reader = csv.DictReader(args.pdblist,delimiter='\t')

data = [x for x in dict_reader]
subtypes = set([x['Subtype'] for x in data])

cwd = os.getcwd()

for subtype in subtypes:
    if not os.path.exists(subtype):
        os.mkdir(subtype)

# Create each strain dir
for subtype in subtypes:
    os.chdir(subtype)
    strain_list = set([x['Strain'] for x in data if x['Subtype'] == subtype])
    for strain in strain_list:
        strain = re.sub('/','_',strain)
        if not os.path.exists(strain):
            os.mkdir(strain)
        os.chdir(strain)
        pdb_list = set([x['PDB ID'] for x in data if x['Subtype'] == subtype \
                                                 and x['Strain'] == strain])
        for pdb in pdb_list:
            # call getentry for each subtype / strain / pdbid list
            os.system('getentry -b ' + pdb)
        for filename in os.listdir(os.getcwd()):
            if os.path.isfile(filename):
                os.system('gunzip ' + filename)
        os.chdir('..')
    os.chdir('..')
    

