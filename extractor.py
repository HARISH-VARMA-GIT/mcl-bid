import mcl_ca as mclc
import mcl_gstin as mclg 
import mcl_legal as mcll
import mcl_pan as mclp
import mcl_attorney as mcla
import mcl_dsc as mcld
import mcl_workcap as mclw
import nit
import mcl_undertaking as mcl_under

links = {
    "gst": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1683525563/4_GST_registration_m6gmz8.pdf",
    "pan": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1683525563/3_Permanent_Account_Number_chmph4.pdf",
    "affidavit": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1683097817/7_Affidavit_zhzf6p.pdf",
    "workcap": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1683525563/2_Working_Capital1_vv1t8f.pdf",
    "dsc": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1683525563/6_Digital_Signature_Certificate_va9fu0.pdf",
    "ca": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1683525563/CACERTIFICATE1920_vyuxuu.pdf",
    "legal": "https://bidderdocbucket.s3.ap-south-1.amazonaws.com/5_Legal_Status_of_the_bidder+(1).pdf",
    "undertaking": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1685211070/8_Undertaking_mclgk2.pdf",
    "nit": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1685207217/NIT_164_lgyba2.pdf",
    "gtc": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1685384024/GTC_164_eaj1gd.pdf"
}

class CivilExtractor:
    nit_desc = {}
    gtc = ""
    
    def extract_info_from_ca(self, filepath):
        return mclc.extract_from_CA(filepath)

class CMCExtractor:   
    nit_desc = {}
    gtc = ""
    def __init__(self, nit_path, gtc_path) -> None:
        n = nit.NITDocument(nit_path)
        self.nit_desc = n.extract_info()
        self.gtc = mcl_under.extract_gtc_undertaking(gtc_path)
        
    def extract_pan(self, filepath):
        return mclp.getPAN(filepath)
    
    def extract_gstin(self, filepath):
        return mclg.getGSTIN(filepath)
    
    def extract_info_from_legal(self, filepath):
        return mcll.extract_from_legal(filepath)
    
    def extract_from_affidavit(self, filepath):
        return mcla.extract_attorney_desc(filepath, self.nit_desc["Work Description"])
    
    def extract_from_dsc(self, filepath):
        return mcld.extract_from_dsc(filepath)
    
    def extract_workcap(self, filepath):
        return mclw.extract_workcap(filepath)
    
    def check_undertaking(self, filepath):
        return mcl_under.compare_undertakings(filepath, self.gtc)