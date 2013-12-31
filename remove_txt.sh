#!/bin/bash
# Removes .txt from all files in ls
for a in $( ls ); do mv $a ${a%.txt} ; done
