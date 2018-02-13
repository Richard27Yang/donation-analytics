# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 21:23:57 2018
This module include all the utilities used by donation_analytics.py
@author: Yunchao Yang
"""
import math
import sys
from datetime import datetime

# function to check if input files is readable and writable
def check_files(donors_input,pcecentile_input,donors_repeat_file):
    ''' check if files name are given correctly '''
    
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

# function to remove empty lines
def nonblank_lines(file_lines):
    ''' remove empty lines '''
    for line in file_lines:
        line_rstp = line.rstrip()
        if line_rstp:
            yield line_rstp

# function to calculate percentile  
def percentile_compute(numbered_list, percentile_set):
    ''' Percentile computation 

    Input: 
            Numbered_list, a sorted list 
            percentile_set, int, desired percentile value
            
    Returns: the ith element in the sorted list corresponding to the  percentile value

    '''
    ith = int(math.ceil(float(percentile_set)/ 100. * len(numbered_list))) 
    return numbered_list[ith- 1]