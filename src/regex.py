import re

""" 
Module for regex operations, extracts summary, skills, work experience, and education.
"""

# Month set for cleaning degree names
month_set = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
]

# Function to extract summary 
def get_summary(text):
    pattern = re.compile(
        r'(?s)(?:Summary|Overview)\s*(.*?)(?=\s*(?:\Z|Work History|Work Experience|Experience|Skills|Core Qualifications|Education|Training|Certification)\b)',
        # re.IGNORECASE
    )
    match = pattern.search(text)
    if match:
        summary = match.group(1).strip().replace('\n', ' ')
        return summary
    return None

# Function to extract skills
def get_skills(text):
    pattern = re.compile(
        r'(?s)(?:Skills|Core Qualifications)\s*(.*?)(?=\s*(?:\Z|Work History|Work Experience|Summary|Overview|Experience|Education|Training|Certification)\b)',
    )
    match = pattern.search(text)
    if match:
        skills = match.group(1).strip().replace('\n', ' ')
        skills_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
        return skills_list
    return None

# Function to extract work experience
def get_experiences(text):
    experience_list = []
    pattern = re.compile(
        r'(?s)(?:Work History|Experience|Work Experience)\s*(.*?)(?=\s*(?:\Z|Summary|Overview|Skills|Core Qualifications|Education|Certification|Training)\b)'
    )
    match = pattern.search(text)
    if not match:
        return None
    
    exp_block = match.group(1).strip()
    
    date_pattern = r"(?:(?:\d{1,2}/\d{4})|(?:[A-Z][a-z]{2,}\s\d{4}))"
    date_range = f"{date_pattern}\\s+to\\s+(?:Current|{date_pattern})"
    delimiter_pattern = f"(^.*?{date_range}.*?$)"
    
    entries = re.split(delimiter_pattern, exp_block, flags=re.MULTILINE | re.IGNORECASE)
    work_entries = []
    for i in range(1, len(entries), 2):
        header = entries[i]
        description = entries[i + 1] if (i + 1) < len(entries) else ""
        
        full_block = header + description
        work_entries.append(full_block)
        
    for i, entry in enumerate(work_entries):
        entry = entry.strip()
        if not entry:
            continue
        
        # Extract job title, company name, and date
        job_title = re.search(r'(?i)(?:(?:(?:|\d{4}|\d{1,2}\/\d{4}|[a-z]{3,}\s\d{4})to\s*(?:current|\d{4}|\d{1,2}\/\d{4}|[a-z]{3,}\s\d{4}))|(?:\s*Company Name\s*,*\s*City\s*,*\s*State\s*))?\s*(.*?)\s*(?:(?:[a-z]{3,}\s\d{4}|\d{1,2}\/\d{4})\s+to|Company Name)', entry)
        company_name = "Company Name"
        if job_title:
            job_title = job_title.group(1).strip()
        else:
            job_title = "Unknown Job Title"
        
        date = re.search(r'(?i)(\d{1,2}\/\d{4}|[a-z]{3,}\s*\d{4})\s+to\s+(current|[a-z]{3,}\s*\d{4}|\d{1,2}\/\d{4})', entry)
        if date:
            date = date.group(0).strip()
        else:
            date = "Unknown Date"
            
        experience_list.append({
            'job_title': job_title,
            'company_name': company_name,
            'date': date
        })
    
    # exp_entries = re.split(r'\n(?=[A-Z][a-zA-Z\s]+, \d{2}\/\d{4})', exp_block.strip()) 
    # experience_list = []
    # for entry in exp_entries:
    #     if not entry.strip():
    #         continue
        
    #     job_title = re.search(r'(?i)(?:(?:(?:|\d{4}|\d{1,2}\/\d{4}|[a-z]{3,}\s\d{4})to\s*(?:current|\d{4}|\d{1,2}\/\d{4}|[a-z]{3,}\s\d{4}))|(?:\s*Company Name\s*,*\s*City\s*,*\s*State\s*))?\s*(.*?)\s*(?:(?:[a-z]{3,}\s\d{4}|\d{1,2}\/\d{4})\s+to()|Company Name)', entry)
    #     company_name = "Company Name"
    #     if job_title:
    #         job_title = job_title.group(1).strip()
    #     else:
    #         job_title = "Unknown Job Title"
             
    #     date = re.search(r'(?i)(\d{1,2}\/\d{4}|[a-z]{3,}\s*\d{4})\s+to\s+(current|[a-z]{3,}\s*\d{4}|\d{1,2}\/\d{4})', entry)
    #     if date:
    #         date = date.group(0).strip()
    #     else:
    #         date = "Unknown Date"
            
    #     experience_list.append({
    #         'job_title': job_title,
    #         'company_name': company_name,
    #         'date': date
    #     })
    
    return experience_list if experience_list else None

# Function to extract education --> needs to be processed further
def get_education(text):
    education = []
    
    pattern = re.compile(
        r'(?s)(?:Education|Academic Background|Training)\s*(.*?)(?=\s*(?:\Z|Work History|Work Experience|Summary|Overview|Experience|Skills|Core Qualifications|Education|Certifications)\b)'
    )
    match = pattern.search(text)
    
    entries = get_education_entries(match.group(1)) if match else []
    
    year_pattern = r"\b((?:19|20)\d{2})\b"
    degree_pattern = r"(\b(?:Bachelor|Master|Associate|Doctorate|Ph\.D|B\.S|M\.S|A\.A|BS|MS|MBA|Certificate|High School Diploma).*?(?=\s*[:,]\s*\d{4}|\s+\b(?:19|20)\d{2}\b|[a-z]{3,}\s*\d{4}|\s+at\s+|\s+\b(?:University|College|School|Institute)\b))"
    university_pattern = r"([\w\s,]+(?:University|College|Institute|School|Academy)[\w\s,]*)"
    
    # pattern1 = re.compile(
    #     f"(?P<degree>{degree_pattern})?"
    #     f"(?P<university>{university_pattern})?"
    #     f"(?P<year>{year_pattern})?",
    #     re.IGNORECASE | re.VERBOSE
    # )

    # pattern2 = re.compile(
    #     f"(?P<degree>{degree_pattern})?"
    #     f"(?P<university>.*)",
    #     re.IGNORECASE | re.VERBOSE
    # )
    
    pattern1 = re.compile(f"(?P<degree>{degree_pattern.replace(')','')} :? .*?)(?:,|,|:)?\\s*(?P<year>{year_pattern})\\s*(?P<university>{university_pattern})", re.IGNORECASE)
    
    pattern2 = re.compile(f"(?P<degree>.*?)(?:,|,|:)?\\s*(?P<year>{year_pattern})\\s*(?P<university>.*)", re.IGNORECASE)

    pattern3 = re.compile(f"(?P<degree>{degree_pattern})\\s*,?\\s*(?:at\\s*)?(?P<university>{university_pattern})", re.IGNORECASE)
    
    pattern4 = re.compile(f"(?P<degree>.*?)(?P<university>{university_pattern})", re.IGNORECASE)

    patterns = [pattern1, pattern2, pattern3, pattern4]
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        match_entry = None
        for pattern in patterns:
            match_entry = pattern.search(entry)
            if match_entry:
                break
        
        if not match_entry:
            continue
        
        # Clean degree names (prone to errors)
        degree = match_entry.group('degree').strip() if match_entry.group('degree') else "Unknown Degree"
        for month in month_set:
            degree = re.sub(f'\\b{month}\\b', '', degree, flags=re.IGNORECASE)
        degree = re.sub(r'\d+', '', degree)
        degree = re.sub(r'\s+', ' ', degree).strip()
        
        university = match_entry.group('university').strip() if match_entry.group('university') else "Unknown University"
        year = match_entry.group('year').strip() if match_entry.group('year') else "Unknown Year"
        
        education.append({
            'degree': degree,
            'university': university,
            'year': year
        })
    
    return education if education else None

def get_education_entries(text):
    entries = []
    splitter = re.compile(
        r"(?=\b(?:Bachelor|B\.S|BS|Master|M\.S|MBA|Associate|A\.A|Ph\.D|Doctorate|High School|Certificate))",
        re.IGNORECASE
    )
    
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        # Split a single line into multiple if it contains multiple degree keywords
        sub_entries = splitter.split(line)
        for entry in sub_entries:
            if entry.strip():
                entries.append(entry.strip())
    return entries

def parse_cv(text):
    data = {
        'summary': get_summary(text),
        'skills': get_skills(text),
        'experiences': get_experiences(text),
        'education': get_education(text)
    }
    return data
