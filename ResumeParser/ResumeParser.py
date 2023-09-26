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
logger_watchtower = logging.getLogger(__name__)

"""# FUNCTION - COMMON, READ PDF"""

def common(words_df):
    words_df['fontname'] = words_df['fontname'].replace('Gautami', 'Calibri-Bold')
    words_df = words_df[words_df['text'] != '\u200b']
    words_df = words_df.reset_index(drop=True)  # Use reset_index to reset the index
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

def read_pdf(path):
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

"""# FUNCTION - SKILLS"""

def create_skills_dict(skills_path):
    skills_dict = {}
    skills = []

    # Read and process the skills file
    with open(skills_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Check if the line is not empty
                skills.append(line.split(','))

    # Extract unique keys from skills
    keysk = [item[0].lower() for item in skills]

    root = []
    main = []

    # Iterate through skills to categorize them
    for s in skills:
        s[0] = s[0].lower()
        w = s[0].split(" ")
        l1 = [x for x in keysk if w == x.split(" ")[:len(w)]]
        if len(l1) > 1:
            root.append(s)
        else:
            main.append(s)

    # Combine root and main skills
    skills = main + root

    # Create a regular expression pattern for matching skills
    pat = r"\b(" + "|".join(re.escape(item[0]) for item in skills) + r")\b"

    # Populate the skills dictionary
    for item in skills:
        skills_dict[item[0]] = [i for i in item[1:] if i]

    return pat, skills_dict



import re

def extract_skills(lines_df_1, pat, skills_dict):
    try:
        # Join text from the DataFrame
        text = " ".join(lines_df_1["text"])

        # Replace non-ASCII characters with spaces
        text = re.sub(r'[^\x00-\x7f]', ' ', text)

        # Convert text to lowercase
        text = text.lower()

        # Replace specific characters with spaces
        text = re.sub(r'[\\|,|/|:|\)|\(|\n]', ' ', text)

        # Find matches for the pattern in the text
        match_sk = re.findall(pat, text, re.IGNORECASE)

        # Remove duplicates from the list
        match_sk = list(dict.fromkeys(match_sk))

        # Sort the list of skills
        match_sk = sorted(match_sk)

        # Extract skill values from the skills dictionary
        sk_val = [skills_dict[x] for x in match_sk]

        # Flatten the list of skill values
        sk_val = [item for sublist in sk_val for item in sublist]

        # Remove duplicates from the flattened list
        match_sk = list(dict.fromkeys(sk_val))

        # Sort the final list of skills
        match_sk = sorted(match_sk)

    except Exception:
        match_sk = []

    return match_sk

def resume_parser(full_path, pat, skills_dict):
    pdfname = re.split(r"\\|\/", full_path)[-1]
    words_df, error_flag, pdf = read_pdf(full_path)
    
    if error_flag == 9999:
        skills = []
    else:
        words_df = common(words_df)
        
        def update_1(rows):
            return " ".join(rows['text']), rows['fontname'].values, rows['size'].values
        
        lines_df_1 = words_df.groupby(['page', 'top']).apply(update_1).reset_index()
        lines_df_1 = pd.DataFrame(lines_df_1[0].tolist(), columns=['text', 'fontname', 'size'])
        lines_df_1['len'] = lines_df_1['text'].apply(lambda x: len(x.split()))
        
        skills = extract_skills(lines_df_1, pat, skills_dict)
    
    output = {"Name": pdfname, "Skills": skills}
    return output



def getMatchedSkills(full_path, pat, skills_dict):
    pdfname = os.path.basename(full_path)
    
    try:
        if pdfname[-3:].lower() == "doc" or pdfname[-4:].lower() == "docx":
            subprocess.check_output(['libreoffice', '--convert-to', 'pdf', full_path], timeout=10)
            full_path = ".".join(full_path.split(".")[:-1]) + ".pdf"
        
        output = resume_parser(full_path, pat, skills_dict)
    
    except Exception as e:
        logger_watchtower.error('Error in resume parsing %s' % str(e))
        
        if str(type(e)) == "<class 'subprocess.TimeoutExpired'>" or \
                str(e) == "Command '['libreoffice', '--convert-to', 'pdf', 'downloadResume.docx']' timed out after 10 seconds":
            os.system("kill -9 `pgrep -lf soffice.bin | awk {'print $1'}`")
    
        output = {"Name": pdfname, "Skills": []}
    
    return output



if __name__ == "__main__":
    # Arg 1 = pdf path, Arg 2 = Skills csv path
    # Removing the name of the file (run.py) from the arguments' list
    argv = sys.argv[1:]
    
    # Check if the correct number of arguments is provided
    if len(argv) < 2:
        print("Usage: python script.py <pdf_path> <skills_csv_path>")
        sys.exit(1)
    
    # Path to resume.pdf
    full_path = str(argv[0])
    
    # Path to skillset.csv file
    skills_path = str(argv[1])
    
    pat, skills_dict = create_skills_dict(skills_path)
    
    pdfname = os.path.basename(full_path)
    
    try:
        if pdfname[-3:].lower() == "doc" or pdfname[-4:].lower() == "docx":
            subprocess.check_output(['libreoffice', '--convert-to', 'pdf', full_path], timeout=10)
            full_path = ".".join(full_path.split(".")[:-1]) + ".pdf"
        
        output = resume_parser(full_path, pat, skills_dict)
    
    except Exception as e:
        if str(type(e)) == "<class 'subprocess.TimeoutExpired'>" or \
                str(e) == "Command '['libreoffice', '--convert-to', 'pdf', 'downloadResume.docx']' timed out after 10 seconds":
            os.system("kill -9 `pgrep -lf soffice.bin | awk {'print $1'}`")
        output = {"Name": pdfname, "Skills": []}
    
    print(output)

