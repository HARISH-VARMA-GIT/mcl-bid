"""
compares the bidder undertaking with the original undertaking format 
returns the similarity value
"""
import mcl_utils as mclu
import spacy

def extract_gtc_undertaking(gtc_path):
    gtc, _, __ = mclu.open_file_link(gtc_path)
    return gtc[58].get_text()

def compare_undertakings(filepath, gtc_undertaking):
    bidder_undertaking = mclu.extract_text(filepath, endpg=1)
    nlp = spacy.load("en_core_web_lg") 
    # can change to en_core_web_md or en_core_web_md if problem in downloading
    rel = mclu.get_answer(bidder_undertaking,
                          "does the compnay have any relative in mcl in yes or no?",
                          cleaning_text=None)
    if "yes" in rel:
        rel = True
    else:
        rel = False
    sim = nlp(bidder_undertaking).similarity(nlp(gtc_undertaking))
    return {
        "any relatives": rel,
        "similarity": sim
    }

