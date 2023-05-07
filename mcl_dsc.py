import mcl_utils as mclu
import re

def extract_from_dsc(filepath):
    filetext = mclu.extract_text(filepath)
    attorney = mclu.get_answer(filetext, "name of the person with power of attorney")
    return re.findall(r'"([^"]*)"', attorney)[0]