import os
from pymol import cmd

cwd = os.getcwd()
files = os.listdir(cwd)
targets = [x for x in files if x[-3:] == 'pdb']

for target in targets:
    cmd.load(target)
