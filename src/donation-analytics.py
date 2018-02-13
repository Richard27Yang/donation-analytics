# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 16:26:25 2018

@author: Yunchao Yang
"""

import sys
from datetime import datetime
from pprint import pprint
from utils import percentile_compute,check_files, nonblank_lines

# class of new record of each line
class New_Record():
    ''' Create an record class 
    
    Parameters
    --------------------
	self, record
	
    Attributes
    --------------------
      cmte_id, 	string, recepient id
      donor_name, string, donor name
      zip_code, string, donor's zip code
      transaction_dt, datetime.date format,  transaction date,%m%d%Y
      year, int, transaction year, 
      transaction_amt, int, transaction amount
      other_id, string, other id input
    '''
    def __init__(self, record):
        self.record = record

    def extract_item_from_record(self):
        ''' Extract item from record 
        
            Parameters
            --------------------
            self
            
            Returns
            self: object or None if record length is not right
            --------------------
        
        '''
        line = self.record
        words = line.split('|')
        if len(words) != 21:
            print("The record length is not valid",line)
            return None
        else:
            self.cmte_id = words[0].strip()
            self.donor_name = words[7].strip()
            self.zip_code = words[10][:5]
            try:
                self.transaction_dt = datetime.strptime(words[13],'%m%d%Y').date()
                self.year = self.transaction_dt.year
            except:
                self.transaction_dt = None                
            try: 
                self.transaction_amt = int(round(float(words[14].strip())))
            except:
                self.transaction_amt = None
            self.other_id = words[15].strip()
        return self
    
    def check_valid_record(self):
        '''check if record is valid
            Parameters
            --------------------
            self
            
            Returns
                -True, if record is valid
                -False record is not valid
            '''
        
        if self.other_id:
            return False
        if not self.cmte_id or not self.donor_name or not self.zip_code or not self.transaction_dt or not self.transaction_amt:
            return False
        if len(self.zip_code) != 5:
            return False
        if self.transaction_amt < 1:
            return False
    
        return True
    
    
if __name__ == '__main__':
    
    # check proper input 
    try:
        donors_input = sys.argv[1] 
        pcecentile_input = sys.argv[2]
        donors_repeat_file = sys.argv[3]
    except IndexError:
        print("!!! Please input the files using the correct format: 1) donation input file, 2) percentile input file, 3) output file")
        print("Eg: python ./src/donation-analytics.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt")
        sys.exit()  
    
    # test input or output file read and write availability
    check_files(donors_input,pcecentile_input,donors_repeat_file)
    
    write_repeat_file = open(donors_repeat_file,'w')
    with open(pcecentile_input, 'r') as per_input:
        try:
            percentile = int(per_input.read())
            #print(percentile)
            if(percentile > 100 or percentile < 0 ):
                raise ValueError("The input percentile %d is not valid (0-100)" % (percentile) )
        except IOError:
            print("The percentile value is not correct. \n")
    num, repeat_num = 0, 0
    donor_id_dict=[]
    recepient_dict=[]
    total_amount = 0
    repeat_donor_list = []
    with open(donors_input,'r') as donors_input_records:
  #      all_records = csv.reader(donors_input_records,delimiter='|')
        for each_record in nonblank_lines(donors_input_records):
            record = New_Record(each_record)
            record = record.extract_item_from_record()
            #pprint(vars(record))
            if record is not None and record.check_valid_record():
                num += 1
                print('col' + str(num))
                
                if (record.donor_name,record.zip_code) not in donor_id_dict:
                    # donor_id_dict.append((record.donor_name,record.zip_code))
                    donor_id_dict.append((record.donor_name,record.zip_code))
                else:
                    repeat_num += 1
                    total_amount = total_amount + record.transaction_amt
                    repeat_donor_list.append(record.transaction_amt)
                    repeat_donor_list.sort()
                    perc = percentile_compute(repeat_donor_list, percentile)
                    donor_repeat_record = record.cmte_id +'|'+record.zip_code +'|'+str(record.year)+'|'+ str(perc) +'|'+ str(total_amount) + '|' + str(repeat_num) +'\n'
                    print(donor_repeat_record)
                    write_repeat_file.write(donor_repeat_record)              
    print(donor_id_dict)
    print(repeat_donor_list)    
        
        
        
        