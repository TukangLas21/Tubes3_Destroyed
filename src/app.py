import time

from connector import Connector
from encryption import Encryption
from pdf_processor import extract_text_regex, extract_text_strmatching
from regex_func import parse_cv
from algorithm.fuzzy import fuzzy_search
from algorithm.bm import BoyerMoore
from algorithm.ac import AhoCorasick
from algorithm.kmp import KMP
from collections import Counter

def exact_search(keywords, cv_texts, algorithm):
    search_result = {
        detail_id: {
            "detail_id": detail_id,
            "applicant_id": cv_data['applicant_id'],
            "cv_path": cv_data['cv_path'],
            "keywords_matches": {}
        } for detail_id, cv_data in cv_texts.items()
    }
    keywords_found = set()
    
    if algorithm == "AC":
        keywords_list = list(keywords)
        ac = AhoCorasick(keywords_list)
    
    for detail_id, cv_data in cv_texts.items():
        text = cv_data['text']
        
        if algorithm == "AC":
            found_patterns = ac.search_detailed(text)
            if found_patterns:
                keywords_count = Counter(item['val'] for item in found_patterns)
                for keyword, count in keywords_count.items():
                    search_result[detail_id]["keywords_matches"][keyword] = [count, "exact"]
                    keywords_found.add(keyword)
                    
        else:
            for keyword in keywords:
                num_matches = 0
                if algorithm == "KMP":
                    num_matches = KMP(text, keyword)
                elif algorithm == "BM":
                    num_matches = BoyerMoore(text, keyword)
                
                if num_matches > 0:
                    search_result[detail_id]["keywords_matches"][keyword] = [num_matches, "exact"]
                    keywords_found.add(keyword)
            
    return search_result, keywords_found

def fuzzy_search_start(keywords, cv_texts, exact_search_result, percentage=75.0):

    for detail_id, cv_data in cv_texts.items():
        text = cv_data['text']
        for keyword in keywords:
            if keyword in exact_search_result[detail_id]["keywords_matches"]:
                continue
            
            num_matches = fuzzy_search(text, keyword, percentage)
            if num_matches > 0:
                exact_search_result[detail_id]["keywords_matches"][keyword] = [num_matches, "fuzzy"]
                
    return exact_search_result

# Main function to start the search process
def start_search(keywords, algorithm, all_cv_info, number_of_results, connector: Connector):
    keywords_list = {keywords.strip() for keywords in keywords.split(',') if keywords.strip()}
    if not keywords_list:
        return None
    
    cv_texts = {}
    for detail_id, applicant_id, cv_path in all_cv_info:
        try:
            text = extract_text_strmatching(cv_path)
            if not text:
                raise ValueError(f"Could not extract text from CV at {cv_path}")
            cv_texts[detail_id] = {
                "applicant_id": applicant_id,
                "cv_path": cv_path,
                "text": text
            }
        except Exception as e:
            print(f"Error processing CV at {cv_path}: {e}")
            continue
            
    exact_start = time.time()
    search_result, keywords_found = exact_search(keywords_list, cv_texts, algorithm)
    exact_end = time.time()
    exact_time = exact_end - exact_start
    
    keywords_not_found = keywords_list - keywords_found
    
    fuzzy_start = fuzzy_end = 0
    if keywords_not_found:
        fuzzy_start = time.time()
        search_result = fuzzy_search_start(keywords_not_found, cv_texts, search_result)
        fuzzy_end = time.time()
        
    final_results = []
    for detail_id, result in search_result.items():
        result['accuracy_score'] = len(result['keywords_matches'])
        if result['accuracy_score'] > 0:
            final_results.append(result)
            
    final_results.sort(key=lambda x: x['accuracy_score'], reverse=True)
    sorted_results = final_results[:number_of_results]
    
    try:
        connector.connect()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None 
    
    # Get applicant profiles for the results
    for result in sorted_results:
        applicant_id = result['applicant_id']
        profile = connector.get_decrypted_profile(applicant_id)
        result['profile'] = profile if profile else {
            "first_name": "Unknown",
            "last_name": "Unknown",
            "address": "Unknown",
            "phone_number": "Unknown"
        }
    connector.close()
    
    return {
        "results": sorted_results,
        "exact_time": exact_time,
        "fuzzy_time": fuzzy_end - fuzzy_start if keywords_not_found else 0     
    }

def get_cv_text(cv_path):
    text = extract_text_regex(cv_path)
    if not text:
        return None
    
    return text.strip()
    
def get_cv_info(cv_path):
    text = get_cv_text(cv_path)
    if not text:
        return None
    
    cv_info = parse_cv(text)
    if not cv_info:
        return None
    
    return cv_info


