import io
from PIL import Image

def pdf2img(filepath):  
  # ocr cannot work on pdf format. so converting it to a suitable image format
    pdf_file = fitz.open(filepath)
    filename = filepath.split("/")[-1].split(".")[0]
    images_extracted = []
    # iterate over PDF pages
    for page_index in range(len(pdf_file)):
        # get the page itself
        page = pdf_file[page_index]
        image_list = page.get_images()
        # printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.get_images(), start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # save it to local disk
            image_name = f"{filename}P{page_index}I{image_index}.{image_ext}"
            image.save(open(image_name, "wb"))
            images_extracted.append(image_name)
    return images_extracted

import easyocr  # for optical character recognition
import os

def extract_text(filepath):
  reader = easyocr.Reader(['en'], gpu=True)
  pages = pdf2img(filepath)
  result = ""
  for imagepath in pages:
    text_extracted = reader.readtext(imagepath, paragraph="False")
    for txt in text_extracted:
      result += "\n" + txt[-1]
    os.remove(imagepath)
  return result

import fitz
import re

def getGSTIN(filepath):
  doc = fitz.open(filepath)
  text = ""
  for page in doc:
    text += page.get_text()
  if text == "":
    text = extract_text(filepath)
  gst = re.findall(r"Registration Number[ ]*:[ ]*([a-zA-Z0-9]+)|Registration Number[ ]*([a-zA-Z0-9]+)", text)
  gstin_extracted = []
  for g in gst:
    if g[0] == "" and g[1] == "":
      gstin_extracted.append("")
    elif g[0] == "":
      gstin_extracted.append(g[1])
    else:
      gstin_extracted.append(g[0])
  return gstin_extracted
