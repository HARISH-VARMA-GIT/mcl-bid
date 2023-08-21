import mcl_utils as mclu

def extract_udayam(filepath):
    filetext = mclu.extract_text(filepath, endpg=1)
    enterprise_type = mclu.get_answer(filetext, "type of enterprise")
    regis_no = mclu.get_answer(filetext,"udyam registration number")
    enterprice_name = mclu.get_answer(filetext,"name of enterprise")
    nic = mclu.get_answer(filetext,"nic 2 digit")
    info_extracted = {
      "Type of Enterprise": enterprise_type,
      "Udyam Registration Number": regis_no,
      "Name of Enterprise": enterprice_name,
      "Nic 2 Digit": nic
    }
    return info_extracted
