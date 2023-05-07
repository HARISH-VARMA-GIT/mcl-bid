import os
import re
import mcl_utils as mclu



import easyocr  # for optical character recognition
def extract_text_easyocr(imagepath):
  reader = easyocr.Reader(['en'], gpu=True)
  text_extracted = reader.readtext(imagepath, paragraph="False")
  result = []
  for txt in text_extracted:
    result.append(txt[-1])
  return result

def getPAN(imagepath):
  potential_changes = {"S": "5",
                     "I": "1",
                     "O": "0",
                     "Z": "2",
                     "B": "8",
                     "T": "7",
                     "A": "4",
                     "l": "1"}
  images = mclu.pdf2img(imagepath)
  pan = []
  for img in images:
    text = extract_text_easyocr(img)
    for txt in text:
      for t in txt.split():
        if len(t) == 10:
          pan.append(t)

  for img in images:
    os.remove(img)
  pan_changed = []
  for p in pan:
    dig = p[-5: -1]
    dig_changed = ""
    for d in dig:
      if d.isalpha() and d in potential_changes.keys():
        dig_changed += potential_changes[d]  # compensating for bad image quality that causes poor character recognition
        # this still does not eliminate the whole problem... it still may not work in some cases
      else:
        dig_changed += d
    pan_changed.append(p[: -5] + dig_changed + p[-1])
  pan = set()
  for p in pan_changed:
    t = re.findall(r"[A-Z][A-Z][A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9][A-Z]", p)  # regular expression for PAN number verification
    if len(t) != 0:
      pan.add(t[0])
  return pan

