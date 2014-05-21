#!/usr/bin/python
"""
Creates a base directory structure ala Project Template (from R)
author - Devin Villegas
2013/08/19

"""

import argparse
import errno
import os
import sys

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

parser = argparse.ArgumentParser(description='Create a data analysis directory structure')

parser.add_argument('project_name',help='Name of the project we are creating')
args = parser.parse_args()
project_name = args.project_name

cwd = os.getcwd()
target = cwd + '/' + project_name


# Check if we are going to overwrite a directory
current_dirs = os.listdir(cwd)
if args.project_name in current_dirs:
    print "Current project name exists in dir"

# Confirm location to create template
ans = raw_input("Confirm creating " + project_name + " project in " + cwd + ": y/[n]\n")
if ans.lower() != 'y':
    print "Aborting"
    sys.exit(1)

# Create directory structure
dirs = ['cache','config','data','diagnostics',
        'doc','figures','lib','logs','munge',
        'profiling','reports','scratch','src',
        'tests']
make_sure_path_exists(target)
for elem in dirs:
    create_dir = target + '/' + elem
    print "Creating " + create_dir
    make_sure_path_exists(create_dir)

# Create subdirs
make_sure_path_exists(target + '/figures/exploratory')
make_sure_path_exists(target + '/figures/final')

print 'Writing README'
fh1 = open(target + '/README.md','w')
fh1.write('README File for ' + project_name)
fh1.close()

print 'Writing TODO'
fh2 = open(target + '/TODO.md','w')
fh2.write('TODO File for ' + project_name)
fh2.close()
