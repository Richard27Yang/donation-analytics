# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 21:23:57 2018

@author: yangy
"""
import math
import sys
from datetime import datetime

# Step1 preprocessing: check if input files are ready to read and write
def check_files(donors_input,pcecentile_input,donors_repeat_file):
    '''
    check if files name are given correctly
    
    '''
    
    # check input files availability.
    try:
        fileinput = open(donors_input, 'r')
        fileinput.close()
    except IOError:
        print("There is error reading the he donors input file \n")
        sys.exit()
    try:
        fileinput = open(pcecentile_input, 'r')
        fileinput.close()
    except IOError:
        print("There is error reading the he pcecentile input file \n")
        sys.exit()
    # check output files availability.
    try:
        fileinput = open(donors_repeat_file, 'w')
        fileinput.close()
    except IOError:
        print("There is error reading the he donors donors repeat  file \n")
        sys.exit()
        
    return True

def nonblank_lines(file_lines):
    ''' remove empty lines    
    '''
    for line in file_lines:
        line_rstp = line.rstrip()
        if line_rstp:
            yield line_rstp

def percentile_compute(numbered_list, percentile_set):
    ''' Percentile computation 

    Input: 
            Numbered_list, a sorted list 
            percentile_set, int, desired percentile value
            
    Returns: the ith element in the sorted list corresponding to the  percentile value

    '''
    ith = int(math.ceil(float(percentile_set)/ 100. * len(numbered_list))) 
    return numbered_list[ith- 1]