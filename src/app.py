import time

from connector import Connector
from encryption import Encryption
from pdf_processor import extract_text_regex, extract_text_strmatching
from algorithm.fuzzy import fuzzy_search
from algorithm.bm import BoyerMoore
from algorithm.ac import AhoCorasick
from algorithm.kmp import KMP


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
    
    for detail_id, cv_data in cv_texts.item():
        text = cv_data['text']
        for keyword in keywords:
            num_matches = 0
            if algorithm == "KMP":
                num_matches = KMP(text, keyword)
            elif algorithm == "BM":
                num_matches = BoyerMoore(text, keyword)
            elif algorithm == "AC":
                ac = AhoCorasick([keyword])
                num_matches = ac.search(text)
            else:
                raise ValueError(f"Unknown algorithm: {algorithm}")
            
            if num_matches > 0:
                search_result[detail_id]["keywords_matches"][keyword] = [num_matches, "exact"]
                keywords_found.add(keyword)
            
    return search_result, keywords_found

def fuzzy_search(keywords, cv_texts, exact_search_result, percentage=75.0):

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
def start_search(keywords, algorithm, all_cv_info, number_of_results):
    keywords_list = {keywords.strip() for keywords in keywords.split(',') if keywords.strip()}
    if not keywords_list:
        return None
    
    cv_texts = {}
    for cv_info in all_cv_info:
        raw_text = extract_text_strmatching(cv_info['cv_path'])
        if raw_text:
            cv_texts[cv_info['detail_id']] = {
                'applicant_id': cv_info['applicant_id'],
                'cv_path': cv_info['cv_path'],
                'text': raw_text
            }
            
    exact_start = time.time()
    search_result, keywords_found = exact_search(keywords_list, cv_texts, algorithm)
    exact_end = time.time()
    exact_time = exact_end - exact_start
    
    keywords_not_found = keywords_list - keywords_found
    
    if keywords_not_found:
        fuzzy_start = time.time()
        search_result = fuzzy_search(keywords_not_found, cv_texts, search_result)
        fuzzy_end = time.time()
        
    final_results = []
    for detail_id, result in search_result.items():
        result['accuracy_score'] = len(result['keywords_matches'])
        if result['accuracy_score'] > 0:
            final_results.append(result)
            
    final_results.sort(key=lambda x: x['accuracy_score'], reverse=True)
    
    return {
        "results": final_results[:number_of_results],
        "exact_time": exact_time,
        "fuzzy_time": fuzzy_end - fuzzy_start if keywords_not_found else 0
        
    }