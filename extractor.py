import mcl_ca as mclc
import mcl_gstin as mclg 
import mcl_legal as mcll
import mcl_pan as mclp
import mcl_attorney as mcla
import mcl_dsc as mcld
import mcl_workcap as mclw
import nit
import mcl_undertaking as mcl_under
import civil_attorney as civ_attorney
import gem_udayam 

links = {
    "cmc_gst": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1683525563/4_GST_registration_m6gmz8.pdf",
    "cmc_pan": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1683525563/3_Permanent_Account_Number_chmph4.pdf",
    "cmc_affidavit": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1683097817/7_Affidavit_zhzf6p.pdf",
    "cmc_workcap": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1683525563/2_Working_Capital1_vv1t8f.pdf",
    "cmc_dsc": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1683525563/6_Digital_Signature_Certificate_va9fu0.pdf",
    "legal": "https://bidderdocbucket.s3.ap-south-1.amazonaws.com/5_Legal_Status_of_the_bidder+(1).pdf",
    "undertaking": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1685211070/8_Undertaking_mclgk2.pdf",
    "cmc_nit": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1685207217/NIT_164_lgyba2.pdf",
    "cmc_gtc": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1685384024/GTC_164_eaj1gd.pdf",
    
    "civil_local": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1687108302/mcl/Local_md3c9k.pdf",
    "civil_gtc": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1686230099/AllPartnershipDeed_sax5vl.pdf",
    "civil_ca": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1683525563/CACERTIFICATE1920_vyuxuu.pdf",
    "civil_gst": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1686230093/gst_q5gy9e.pdf",
    "civil_pan": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1686230092/PANCARD_zwer8f.pdf",
    "civil_undertaking": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1686230093/Undertaking_tffghb.pdf",
    "civil_nit": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1686230092/Tendernotice_3_3_phbxvz.pdf",
    "civil_affidavit": "https://res.cloudinary.com/dauxdhnsr/image/upload/v1686230093/POWEROFATTORNEYARUNVERMA2021_on0z1f.pdf"
}

class Extractor:
    def extract_pan(self, filepath):
        return mclp.getPAN(filepath)
    
    def extract_gstin(self, filepath):
        return mclg.getGSTIN(filepath)
    
    def extract_info_from_legal(self, filepath):
        return mcll.extract_from_legal(filepath)

class CivilExtractor(Extractor):
    nit_desc = {}
    gtc = ""
    
    def __init__(self, nit_path):
        n = nit.CivilNITDoc(nit_path)
        self.nit_desc = n.extract_info()
        
    def extract_info_from_ca(self, filepath):
        return mclc.extract_from_CA(filepath)
    
    def extract_attorney(self, filepath):
        return civ_attorney.extract_attorney(filepath)  
    
    def extract_local_content(self, filepath):
        return mcl_under.extract_local_content(filepath)
    
    
class CMCExtractor(Extractor):   
    nit_desc = {}
    gtc = ""
    def __init__(self, nit_path, gtc_path) -> None:
        n = nit.CMCNITDoc(nit_path)
        self.nit_desc = n.extract_info()
        self.gtc = mcl_under.extract_gtc(gtc_path)
    
    def extract_from_affidavit(self, filepath):
        return mcla.extract_attorney_desc(filepath, self.nit_desc["Work Description"])
    
    def extract_from_dsc(self, filepath):
        return mcld.extract_from_dsc(filepath)
    
    def extract_workcap(self, filepath):
        return mclw.extract_workcap(filepath)
    
    def check_undertaking(self, filepath):
        return mcl_under.compare_genuineness(filepath, self.gtc)
    

class GEMExtractor(Extractor):
    def extract_from_udayam(self,filepath):
        return gem_udayam.extract_udayam(filepath)
