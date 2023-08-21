import mcl_utils as mclu
import re
import os

def extract_udayam(filepath):
    activity_dictionary = {
        49: "Land transport and transport via pipelines",
        58: "Publishing activities",
        69: "Legal and accounting activities",
        74: "Other professional, scientific and technical activities",
        77: "Rental and leasing activities",
        78: "Employment activities",
        79: "Travel agency, tour operator and other reservation service activities",
        81: "Services to buildings and landscape activities",
        82: "Office administrative, office support and other business support activities",
        96: "Other personal service activities"
        # ... rest of the dictionary ...
    }
    info_extracted = {}
    filetext = ""
    images = mclu.pdf2img(filepath)
    for image_path in images:
        filetext += " ".join(mclu.extract_text_easyocr(image_path))
        os.remove(image_path)
    #print("filetext: ", filetext, sep="\n")
    matches = re.findall(r"UDYAM-[A-Z]{2}-\d{2}-\d{7}", filetext)
    if matches == []:
        print("Not able to extract text")
    else:
        enterprise_type = mclu.get_answer(filetext, "type of enterprise")
        matches = re.findall(r"UDYAM-[A-Z]{2}-\d{2}-\d{7}", filetext)
        enterprice_name = mclu.get_answer(filetext, "name of enterprise (remove MIS)")
        found_activities = []  # Reset for each image
        nic_pattern = r'\b\d{2}(?!\d)\b'  # Match exactly 2 digits
        nic_pattern1 = r'\b\d{4}(?!\d)\b'  # Match exactly 4 digits
        nic_pattern2 = r'\b\d{5}(?!\d)\b'  # Match exactly 5 digits
        nic_pattern3 = r'\b\d{2}[A-Za-z0-9]{3}(?!\d)\b'
        nic_matches = re.findall(nic_pattern,filetext)
        #print(nic_matches)
        nic_matches1 = re.findall(nic_pattern1,filetext)
        #print(nic_matches1)
        nic_matches2 = re.findall(nic_pattern2,filetext)
        #print(nic_matches2)
        nic_matches3 = re.findall(nic_pattern3,filetext)
        #print(nic_matches3)
        for code in activity_dictionary:
            str_code = str(code)
            if str_code == nic_matches or any(str_code == match[:2] for match in nic_matches1) or any(str_code == match[:2] for match in nic_matches2) or any(str_code == match[:2] for match in nic_matches3):
                found_activities.append(f"{code} - {activity_dictionary[code]}")

        info_extracted = {
            "Type of Enterprise": enterprise_type,
            "Udyam Registration Number": matches,
            "Name of Enterprise": enterprice_name,
            "Nic 2 Digit": found_activities
            }
        print(info_extracted)

pdf_url = "https://res.cloudinary.com/dauxdhnsr/image/upload/v1691221391/mcl/1665400660_loei8r.pdf"
extract_udayam(pdf_url)
