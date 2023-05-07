import fitz
from PIL import Image
import pytesseract
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import requests
import openai
import io
import re
import spacy

openai.api_key = "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"
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extract_text(filepath, startpg=1, endpg=None):
  filestream = io.BytesIO(requests.get(filepath).content)
  file = fitz.open(stream=filestream, filetype="pdf")
  filename = filepath.split("//")[-1].split(".")[0]
  fileloc = "\\".join(filepath.split("\\")[:-1])
  if endpg == None:
      endpg = len(file)
  text = ""
  images = []
  for i in range(startpg-1, endpg):
      pix = file[i].get_pixmap()
      imgloc = fileloc + "\\" + filename + str(i) + ".jpg"
      images.append(imgloc)
      pix.save(imgloc, "JPEG")
  for img in images:
      page_text = pytesseract.image_to_string(Image.open(img))
      text += " -- " + page_text
      os.remove(img)
  return text

def get_answer(context, question):
  prompt = context + " What is the" + question + " in the above text? Say just the" + question + " in quotation marks or parentheses."
  return openai.ChatCompletion.create(
      messages=[{
          "role": "assistant",
          "content": prompt
      }],
      temperature=0,
      max_tokens=300,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      model="gpt-3.5-turbo"
  )["choices"][0]["message"]["content"]

def extract_from_affidavit(filepath, nit_desc):
    filetext = extract_text(filepath)
    attorney = get_answer(filetext, "name of the attorney")
    bidder_desc = get_answer(filetext, "description of the work")
    
    attorney = re.findall(r'"([^"]*)"', attorney)[0]
    bidder_desc = re.findall(r'"([^"]*)"', bidder_desc)[0]
    
    nlp = spacy.load("en_core_web_sm")
    nit = nlp(nit_desc)
    bidder = nlp(bidder_desc)
    
    sim = nit.similarity(bidder)
    similar = False
    if sim >= 0.88:
        similar = True
    output = {
                "attorney": attorney,
                "similar work": similar
    }
    return output

tender_desc = """Hiring of HEMMs (Shovels, Dumpers, Drills, Dozers, 
Graders, Fog Canons etc.) for transfer & transportation 
of materials in various strata including drilling, 
excavation, dumping, spreading, dozing and other allied 
works in specified areas for dumping for exposing 
various coal seams from surface, down to seam II B at 
Ananta OCP as per the instructions of Project 
Officer/Management of Ananta OCP, Jagannath Area, 
MCL,"""

filepath = "https://res.cloudinary.com/dauxdhnsr/image/upload/v1683097817/7_Affidavit_zhzf6p.pdf"
attorneydoc = extract_from_affidavit(filepath, tender_desc)
print(attorneydoc)
