# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 21:19:14 2023

@author: mukhe
"""

import mcl_ca as mclc
import mcl_gstin as mclg 
import mcl_legal as mcll
import mcl_pan as mclp

def extract_pan(filepath):
    return mclp.getPAN(filepath)

def extract_gstin(filepath):
    return mclg.getGSTIN(filepath)

def extract_info_from_ca(filepath):
    return mclc.extract_from_CA(filepath)

def extract_info_from_legal(filepath):
    return mcll.extract_from_legal(filepath)

print(extract_info_from_ca("D:\CV\Project\MCL\Govind Files\civil data1\CACERTIFICATE1920.pdf"))

