import pdfplumber 
import pandas as pd
import numpy as np
from itertools import groupby, count
import re 
import subprocess 
import os
import os.path
import sys
import logging
from tabulate import tabulate
logger_watchtower = logging.getLogger(__name__)
from tqdm import tqdm

class ResumeParser:
    def __init__(self,skills_dict_path,root_directory = None):
        self.root_directory = root_directory
        self.skills_dict_path = skills_dict_path

    def common(self,words_df):
        words_df['fontname'] = words_df['fontname'].replace('Gautami', 'Calibri-Bold')
        words_df = words_df[words_df['text'] != '\u200b']
        words_df = words_df.reset_index(drop=True)
        words_df = words_df[words_df['text'] != '(']
        words_df = words_df[words_df['text'] != ')']
        words_df = words_df.reset_index(drop=True)    
        d = abs(words_df['x1'][:-1] - words_df['x0'][1:].values)
        indices = np.where(d <= 1.0)[0]
        groups = groupby(indices, key=lambda item, c=count(): item - next(c))
        tmp = [list(g) for k, g in groups]
        for i in tmp:
            for j in i:
                words_df.at[i[0], 'text'] = words_df.iloc[i[0]]['text'] + words_df.iloc[j + 1]['text']
        words_df.drop(indices + 1, inplace=True)
        words_df = words_df.reset_index(drop=True)
        d = abs(words_df['top'][:-1].values - words_df['top'][1:].values)
        indices = np.where(d <= 1.5)[0]
        for i in indices:
            words_df.at[i + 1, 'top'] = words_df.at[i, 'top']
        return words_df
    
    def read_pdf(self,path):
        pdf = pdfplumber.open(path)
        words_df = pd.DataFrame()
        error_flag = 0        
        try:
            if len(pdf.pages) >= 10:
                limit_page = 10
            else:
                limit_page = len(pdf.pages)
            for idx in range(limit_page):
                page = pdf.pages[idx]
                words = page.extract_words(x_tolerance=1, y_tolerance=1, keep_blank_chars=False, use_text_flow=True,
                                          extra_attrs=["fontname", "size"])
                page.flush_cache()
                if len(words) > 0:
                    temp = pd.DataFrame.from_dict(words)
                    temp['page'] = idx
                    words_df = pd.concat([words_df, temp])
        except Exception as e:
            error_flag = 9999
            logger_watchtower.error(f"Error reading PDF: {str(e)}")
        if len(words_df) == 0:
            error_flag = 9999
        return words_df, error_flag, pdf

    def create_skills_dict(self):
        skills_dict = {}
        skills = []    
        with open(self.skills_dict_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:  
                    skills.append(line.split(','))        
        keysk = [item[0].lower() for item in skills]
        root = []
        main = []        
        for s in skills:
            s[0] = s[0].lower()
            w = s[0].split(" ")
            l1 = [x for x in keysk if w == x.split(" ")[:len(w)]]
            if len(l1) > 1:
                root.append(s)
            else:
                main.append(s)
        skills = main + root        
        pat = r"\b(" + "|".join(re.escape(item[0]) for item in skills) + r")\b"        
        for item in skills:
            skills_dict[item[0]] = [i for i in item[1:] if i]
        return pat, skills_dict

    def extract_skills(self,lines_df_1, pat, skills_dict):
        try:            
            text = " ".join(lines_df_1["text"])            
            text = re.sub(r'[^\x00-\x7f]', ' ', text)            
            text = text.lower()            
            text = re.sub(r'[\\|,|/|:|\)|\(|\n]', ' ', text)            
            match_sk = re.findall(pat, text, re.IGNORECASE)            
            match_sk = list(dict.fromkeys(match_sk))            
            match_sk = sorted(match_sk)            
            sk_val = [skills_dict[x] for x in match_sk]            
            sk_val = [item for sublist in sk_val for item in sublist]            
            match_sk = list(dict.fromkeys(sk_val))            
            match_sk = sorted(match_sk)
        except Exception:
            match_sk = []
        return match_sk
    
    def resume_parser(self,full_path, pat, skills_dict):
        pdfname = re.split(r"\\|\/", full_path)[-1]
        words_df, error_flag, pdf = self.read_pdf(full_path)
        if error_flag == 9999:
            skills = []
        else:
            words_df = self.common(words_df)
            def update_1(rows):
                return " ".join(rows['text']), rows['fontname'].values, rows['size'].values
            lines_df_1 = words_df.groupby(['page', 'top']).apply(update_1).reset_index()
            lines_df_1 = pd.DataFrame(lines_df_1[0].tolist(), columns=['text', 'fontname', 'size'])
            lines_df_1['len'] = lines_df_1['text'].apply(lambda x: len(x.split()))
            skills = self.extract_skills(lines_df_1, pat, skills_dict)
        output = {"Name": pdfname, "Skills": skills}
        return output

    def getMatchedSkills(self,full_path, pat, skills_dict):
        pdfname = os.path.basename(full_path)        
        try:
            if pdfname[-3:].lower() == "doc" or pdfname[-4:].lower() == "docx":
                subprocess.check_output(['libreoffice', '--convert-to', 'pdf', full_path], timeout=10)
                full_path = ".".join(full_path.split(".")[:-1]) + ".pdf"
            output = self.resume_parser(full_path, pat, skills_dict)
        except Exception as e:
            logger_watchtower.error('Error in resume parsing %s' % str(e))
            if str(type(e)) == "<class 'subprocess.TimeoutExpired'>" or \
                    str(e) == "Command '['libreoffice', '--convert-to', 'pdf', 'downloadResume.docx']' timed out after 10 seconds":
                os.system("kill -9 `pgrep -lf soffice.bin | awk {'print $1'}`")
            output = {"Name": pdfname, "Skills": []}
        return output
    
    def pdf_convertor(self,filename):
        if filename[-3:].lower() == "doc" or filename[-4:].lower() == "docx":
            subprocess.check_output(['libreoffice', '--convert-to', 'pdf', self.resume_path], timeout=10)
            pdf_path = ".".join(self.resume_path.split(".")[:-1]) + ".pdf"
            return pdf_path
        else:
            return filename
    
    def parse_multiple_resumes(self):
        all_resumes = os.listdir(self.root_directory)
        all_outputs = []
        try:
            for resume in all_resumes:
                if not resume.startswith("."):
                    pat, skills_dict = self.create_skills_dict()
                    resume_file_name = os.path.basename(resume)
                    resume_pdf_path = self.pdf_convertor(resume_file_name)
                    resume_pdf_path = os.path.join(self.root_directory,resume)
                    output = resumeparser.resume_parser(resume_pdf_path, pat, skills_dict)
                    all_outputs.append(output)                
        except Exception as e:
            if str(type(e)) == "<class 'subprocess.TimeoutExpired'>" or \
                str(e) == "Command '['libreoffice', '--convert-to', 'pdf', 'downloadResume.docx']' timed out after 10 seconds":
                os.system("kill -9 `pgrep -lf soffice.bin | awk {'print $1'}`")
                output = {"Name": resume, "Skills": []} 
                all_outputs.append(output)
        return all_outputs
    
    def displayer(self, output):
        output_df = pd.DataFrame(output)
        name_df = pd.DataFrame(output_df.iloc[:1]['Name'])
        name_df.rename(columns={'Name':'Skills'},inplace=True)
        name_df['Skills'] = name_df['Skills'].apply(lambda x : '<' * 4 + x.upper() + '>' * 4)
        skills_df = pd.DataFrame(output_df['Skills'])
        skills_df = pd.concat([name_df,skills_df])
        return skills_df



if __name__ == "__main__":
    root = "/Users/pavan/Documents/Resume/"
    masterdf = pd.DataFrame()   
    try:
        resumeparser = ResumeParser(skills_dict_path="skills_dict.csv", root_directory= root)
        outputs = resumeparser.parse_multiple_resumes()
        for output in tqdm(outputs, total = len(outputs), desc = "Parsing Resumes..."):
            skills_df = resumeparser.displayer(output=output)
            masterdf = pd.concat([masterdf,skills_df])
        input("Press Any Key to display results: ")                                    
        print(tabulate(masterdf, tablefmt="fancy_grid",showindex=False))
    except Exception as e:
        print(str(e))
    
