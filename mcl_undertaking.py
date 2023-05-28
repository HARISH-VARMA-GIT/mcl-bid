import fitz
import mcl_utils as mclu
import spacy

def extract_gtc_undertaking(gtc_path):
    gtc_undertaking = ""
    with fitz.open("D:\CV\Project\MCL\Govind Files\\07tend_doc\GTC_164.pdf") as gtc:
        gtc_undertaking =gtc[58].get_text()
    return gtc_undertaking

def compare_undertakings(filepath, gtc_undertaking):
    bidder_undertaking = mclu.extract_text(filepath, endpg=1)
    nlp = spacy.load("en_core_web_sm")
    sim = nlp(bidder_undertaking).similarity(nlp(gtc_undertaking))
    if sim > 0.9:
        return True
    else:
        return False
