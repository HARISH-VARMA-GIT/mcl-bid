import mcl_utils as mclu
import spacy

def extract_attorney_desc(filepath, nit_desc):
    filetext = mclu.extract_text(filepath)
    attorney = mclu.get_answer(filetext, "name of the legal attorney")
    bidder_desc = mclu.get_answer(filetext, "description of the work")
    
    nlp = spacy.load("en_core_web_sm")
    nit = nlp(nit_desc)
    bidder = nlp(bidder_desc)
    sim = nit.similarity(bidder)
    similar = False
    if sim >= 0.8:
        similar = True
    output = {
                "attorney": attorney,
                "similar work": similar
    }
    return output