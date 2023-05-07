import mcl_utils as mclu
import re

#filepath = "D:\CV\Project\MCL\Govind Files\lab system\mcl\MCL data\GODAWARI DEIFY SCMPL JV\\2_Working_Capital1.pdf"

def extract_workcap(filepath):
    filetext = mclu.extract_text(filepath)
    cap = mclu.get_answer(filetext, "working capital")
    cap = float(re.findall(r"\d+.\d*", cap)[0]) * 10000000
    return cap