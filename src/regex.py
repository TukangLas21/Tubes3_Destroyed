import re

""" 
Module for regex operations, extracts summary, skills, work experience, and education.
"""

# Function to extract summary 
def get_summary(text):
    pattern = re.compile(
        r'(?s)(?:Summary|Overview)\s*(.*?)(?=\s*(?:Work History|Work Experience|Experience|Skills|Qualifications|Education|Training|Certification)\b)',
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
        r'(?s)(?:Skills|Qualifications)\s*(.*?)(?=\s*(?:Work History|Work Experience|Summary|Overview|Experience|Education|Training|Certification)\b)',
    )
    match = pattern.search(text)
    if match:
        skills = match.group(1).strip().replace('\n', ' ')
        skills_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
        return skills_list
    return None

# Function to extract work experience --> needs to be processed further
def get_experiences(text):
    pattern = re.compile(
        r'(?s)(?:Work History|Experience|Work Experience)\s*(.*?)(?=\s*(?:Summary|Overview|Skills|Qualifications|Education|Certification|Training)\b)'
    )
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None

# Function to extract education --> needs to be processed further
def get_education(text):
    pattern = re.compile(
        r'(?s)(?:Education|Academic Background|Training|Certification)\s*(.*?)(?=\s*(?:Work History|Work Experience|Summary|Overview|Experience|Skills|Qualifications|Education)\b)'
    )
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None
    