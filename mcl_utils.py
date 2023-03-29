# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 23:31:32 2023

@author: mukhe
"""

import fitz
from PIL import Image
import pytesseract
import os
import openai
from dotenv import dotenv_values
config = dotenv_values(".env")

#openai.api_key = ""
openai.api_key = config["API_KEY"]
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extract_text(filepath, startpg=1, endpg=None):
  file = fitz.open(filepath)
  filename = filepath.split("\\")[-1].split(".")[0]
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