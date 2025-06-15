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

# Fixed main function to start the search process
def start_search(keywords, algorithm, number_of_results):
    print(f"Starting search with keywords: {keywords}, algorithm: {algorithm}, number_of_results: {number_of_results}")
    
    # Validate input parameters
    if not isinstance(keywords, str) or not keywords.strip():
        print("Error: Keywords must be a non-empty string")
        return [], 0, 0
    
    if not isinstance(number_of_results, int) or number_of_results <= 0:
        print("Error: number_of_results must be a positive integer")
        return [], 0, 0
    
    keywords_set = {keyword.strip() for keyword in keywords.split(',') if keyword.strip()}
    if not keywords_set:
        print("Error: No valid keywords found after processing")
        return [], 0, 0
    
    print(f"Processed keywords: {keywords_set}")
    
    try:
        Connector.get_instance().connect()
        all_cv_info = Connector.get_instance().get_paths_id()
        Connector.get_instance().close()
    except Exception as e:
        print(f"Error connecting to database or getting CV paths: {e}")
        return [], 0, 0
    
    if not all_cv_info:
        print("No CV information found in database.")
        return [], 0, 0
    
    print(f"Found {len(all_cv_info)} CVs to process")
    
    cv_texts = {}
    for i in range(len(all_cv_info)):
        detail_id = all_cv_info[i][0]
        applicant_id = all_cv_info[i][1]
        cv_path = all_cv_info[i][2]
        
        try:
            text = extract_text_strmatching(cv_path)
            if not text or not text.strip():
                print(f"Warning: Could not extract text from CV at {cv_path}")
                continue
                
            cv_texts[detail_id] = {
                "applicant_id": applicant_id,
                "cv_path": cv_path,
                "text": text
            }
        except Exception as e:
            print(f"Error processing CV at {cv_path}: {e}")
            continue
    
    if not cv_texts:
        print("No CV texts could be extracted")
        return [], 0, 0
    
    print(f"Successfully processed {len(cv_texts)} CVs")
    
    # Perform exact search
    try:
        exact_start = time.time()
        search_result, keywords_found = exact_search(keywords_set, cv_texts, algorithm)
        exact_end = time.time()
        exact_time = exact_end - exact_start
        
        print(f"Exact search completed in {exact_time:.4f} seconds")
        print(f"Keywords found in exact search: {keywords_found}")
        
    except Exception as e:
        print(f"Error in exact search: {e}")
        return [], 0, 0
    
    # Perform fuzzy search for remaining keywords
    keywords_not_found = keywords_set - keywords_found
    fuzzy_time = 0
    
    if keywords_not_found:
        print(f"Starting fuzzy search for keywords: {keywords_not_found}")
        try:
            fuzzy_start = time.time()
            search_result = fuzzy_search_start(keywords_not_found, cv_texts, search_result)
            fuzzy_end = time.time()
            fuzzy_time = fuzzy_end - fuzzy_start
            print(f"Fuzzy search completed in {fuzzy_time:.4f} seconds")
        except Exception as e:
            print(f"Error in fuzzy search: {e}")
            fuzzy_time = 0
    
    # Process results with better error handling
    final_results = []
    for detail_id, result in search_result.items():
        try:
            # Ensure keywords_matches is a dict
            if not isinstance(result.get('keywords_matches'), dict):
                print(f"Warning: keywords_matches for {detail_id} is not a dict: {type(result.get('keywords_matches'))}")
                result['keywords_matches'] = {}
            
            # Calculate accuracy score safely
            accuracy_score = len(result['keywords_matches'])
            
            # Ensure accuracy_score is an integer
            if not isinstance(accuracy_score, int):
                print(f"Warning: accuracy_score for {detail_id} is not an int: {type(accuracy_score)}")
                accuracy_score = 0
            
            result['accuracy_score'] = accuracy_score
            
            # Only include results with matches
            if accuracy_score > 0:
                final_results.append(result)
                
        except Exception as e:
            print(f"Error processing result for {detail_id}: {e}")
            continue
    
    print(f"Found {len(final_results)} results with matches")
    
    # Sort results safely
    try:
        # Debug: Check the structure of results before sorting
        for i, result in enumerate(final_results[:3]):  # Check first 3 results
            print(f"Result {i} accuracy_score type: {type(result.get('accuracy_score'))}, value: {result.get('accuracy_score')}")
        
        final_results.sort(key=lambda x: x.get('accuracy_score', 0), reverse=True)
        print("Results sorted successfully")
        
    except Exception as e:
        print(f"Error sorting results: {e}")
        # Try to fix the sorting issue
        try:
            # Ensure all accuracy_scores are integers
            for result in final_results:
                if not isinstance(result.get('accuracy_score'), (int, float)):
                    result['accuracy_score'] = 0
            
            final_results.sort(key=lambda x: int(x.get('accuracy_score', 0)), reverse=True)
            print("Results sorted successfully after fixing accuracy_scores")
            
        except Exception as e2:
            print(f"Error in fallback sorting: {e2}")
            # Return unsorted results if sorting fails completely
    
    # Get top results safely
    try:
        # Ensure number_of_results is not larger than available results
        max_results = min(number_of_results, len(final_results))
        sorted_results = final_results[:max_results]
        
        print(f"Selected top {len(sorted_results)} results")
        
    except Exception as e:
        print(f"Error selecting top results: {e}")
        sorted_results = final_results  # Return all results if slicing fails
    
    # Get applicant profiles
    try:
        Connector.get_instance().connect()
        
        for result in sorted_results:
            try:
                applicant_id = result.get('applicant_id')
                if applicant_id:
                    profile = Connector.get_instance().get_decrypted_profile(applicant_id)
                    result['profile'] = profile if profile else {
                        "first_name": "Unknown",
                        "last_name": "Unknown",
                        "address": "Unknown",
                        "phone_number": "Unknown"
                    }
                else:
                    result['profile'] = {
                        "first_name": "Unknown",
                        "last_name": "Unknown",
                        "address": "Unknown",
                        "phone_number": "Unknown"
                    }
            except Exception as e:
                print(f"Error getting profile for applicant {result.get('applicant_id')}: {e}")
                result['profile'] = {
                    "first_name": "Unknown",
                    "last_name": "Unknown",
                    "address": "Unknown",
                    "phone_number": "Unknown"
                }
        
        Connector.get_instance().close()
        
    except Exception as e:
        print(f"Error getting applicant profiles: {e}")
        # Ensure all results have profile data
        for result in sorted_results:
            if 'profile' not in result:
                result['profile'] = {
                    "first_name": "Unknown",
                    "last_name": "Unknown",
                    "address": "Unknown",
                    "phone_number": "Unknown"
                }
    
    print(f"Search completed successfully. Returning {len(sorted_results)} results")
    print(f"Exact search time: {exact_time:.4f} seconds")
    print(f"Fuzzy search time: {fuzzy_time:.4f} seconds")
    
    return sorted_results, exact_time, fuzzy_time

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