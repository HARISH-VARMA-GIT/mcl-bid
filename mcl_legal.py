import mcl_utils as mclu
import time
import re

def extract_from_legal(filepath):
  output = {}
  filetext = mclu.extract_text(filepath, endpg=4)
  jv = mclu.get_answer(filetext, "is the operation a joint venture/consortium in yes or no")
  
  if "yes" in jv.lower():
      companies = mclu.get_answer(filetext, "name of the companies in the joint venture")
      companies = re.findall(r'"([^"]*)"', companies)
      
      for i in range(len(companies)):
          companies[i] = companies[i].replace("$", "").strip()
          
      partnership = {}
      lead = companies[0]
      for c in companies:
        time.sleep(35)
        share = mclu.get_answer(filetext, "partnership share of " + c + " in the joint venture/consortium")
        share = int(re.findall(r"([0-9]+)[ ]*[%]", share)[0])/100
        partnership[c] = share
      for c in companies:
          if partnership[lead] < partnership[c]:
              lead = c
      output = {
                  "JV": True,
                  "partners": partnership,
                  "lead": lead
      }
  
  else:
      companies = mclu.get_answer(filetext, "name of the company in the operation")
      company = re.findall(r'"([^"]*)"', companies)[0]
      output = {
                  "JV": False,
                  "partners": {company: 1},
                  "lead": company
      }
  return output
      
     
