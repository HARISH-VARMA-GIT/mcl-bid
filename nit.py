import re
import camelot as cam

class NITDocument:
    doc = None
    doc_df=[]
    def __init__(self, filepath) -> None:
        self.doc = cam.read_pdf(filepath, 
                                pages = 'all')[:2]
        for i in range(len(self.doc)):
            self.doc_df.append(self.doc[i].df)
            self.doc_df[i].rename(columns=self.doc_df[i].iloc[0], inplace=True)
            self.doc_df[i].drop(self.doc_df[i].index[0], inplace=True)
        
    def extract_dates(self, particular):
          self.doc_df[1]["Particulars"] = self.doc_df[1].Particulars.str.lower()
          x = self.doc_df[1].loc[self.doc_df[1].Particulars==particular.lower()]
          return x.Date.to_string().split("  ")[-1]
    
    def extract_info(self):
        work_desc=self.doc_df[0]
        cost = work_desc.loc[1, 'Estimated Cost of \nWork \n  (In Rs.)']
        cost = float(re.sub(r"[,/-]", "", cost).split()[0])
        completion = int(work_desc.loc[1, 'Period of \nCompletion \n(In Days)'].split()[0])
        desc = re.sub(r"\n", "", work_desc.loc[1, "Description of work"])
        
        return {
            "Cost of Work": cost,
            "Period of Completion (Days)": completion,
            "Work Description": desc,
            "Bid Submission Date": self.extract_dates("Bid Submission start date"),
            "Bid End Date": self.extract_dates("Bid Submission end date"),
            "Tender Publication Data": self.extract_dates('Tender e-Publication date')
        }