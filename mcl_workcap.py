import mcl_utils as mclu
import re

#filepath = "D:\CV\Project\MCL\Govind Files\lab system\mcl\MCL data\GODAWARI DEIFY SCMPL JV\\2_Working_Capital1.pdf"

def extract_workcap(filepath):
    filetext = mclu.extract_text(filepath, endpg=1)
    print(mclu.get_answer(filetext, "working capital",
                          cleaning_text=r"\d+.\d*"))
    cap = float(mclu.get_answer(filetext, "working capital",
                          cleaning_text=r"\d+.\d*")) * 10000000
    udin = re.findall(r'UDIN No[. ]*([A-Z0-9]+)', filetext)[0]
    doctype = mclu.get_answer(filetext, "the document is about")
    return {
        "Working Capital": cap,
        "UDIN No": udin,
        "Type of document": doctype
    }