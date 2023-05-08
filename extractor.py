import mcl_ca as mclc
import mcl_gstin as mclg 
import mcl_legal as mcll
import mcl_pan as mclp
import mcl_attorney as mcla
import mcl_dsc as mcld
import mcl_workcap as mclw

def extract_pan(filepath):
    return mclp.getPAN(filepath)

def extract_gstin(filepath):
    return mclg.getGSTIN(filepath)

def extract_info_from_ca(filepath):
    return mclc.extract_from_CA(filepath)

def extract_info_from_legal(filepath):
    return mcll.extract_from_legal(filepath)

def extract_from_affidavit(filepath, nit_desc):
    return mcla.extract_attorney_desc(filepath, nit_desc)

def extract_from_dsc(filepath):
    return mcld.extract_from_dsc(filepath)

def extract_workcap(filepath):
    return mclw.workcap(filepath)

tender_desc = """Hiring of HEMMs (Shovels, Dumpers, Drills, Dozers, 
Graders, Fog Canons etc.) for transfer & transportation 
of materials in various strata including drilling, 
excavation, dumping, spreading, dozing and other allied 
works in specified areas for dumping for exposing 
various coal seams from surface, down to seam II B at 
Ananta OCP as per the instructions of Project 
Officer/Management of Ananta OCP, Jagannath Area, 
MCL,"""

