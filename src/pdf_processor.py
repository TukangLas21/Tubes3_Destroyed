import fitz
import re
import os

src_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(src_dir)

def extract_text_regex(file_path):
    
    try:
        full_path = os.path.join(root_dir, file_path)
        
        doc = fitz.open(full_path)
        
        full_text = ""
        for page in doc:
            full_text += page.get_text()
            
        doc.close()
        
        return full_text.strip()

    except FileNotFoundError:
        print(f"File '{file_path}' not found. Please ensure the file exists in the specified directory.")
        return None
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")
        return None
    
def extract_text_strmatching(file_path):
    try:
        full_path = os.path.join(root_dir, file_path)
        
        doc = fitz.open(full_path)
        
        full_text = ""
        for page in doc:
            full_text += page.get_text()
            
        doc.close()
        
        full_text = full_text.replace('\n', ' ')
        full_text = re.sub(r'\s+', ' ', full_text).strip().lower()

        return full_text if full_text else None
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Please ensure the file exists in the specified directory.")
        return None
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")
        return None
    

if __name__ == "__main__":
    file_path = input("Enter the path to the PDF file: ")
    text = extract_text_regex(file_path)
    
    if text:
        print("Extracted Text:")
        print(text)
    else:
        print("No text extracted.")
        
    # date = r"(?:(?:\d{1,2}/\d{4})|(?:[A-Z][a-z]{2,}\s\d{4}))"
    
    # date_range = f"{date}\\s+to\\s+(?:Current|{date})"
    
    # delimiter_pattern = f"(^.*?{date_range}.*?$)"
    
    # parts = re.split(delimiter_pattern, text, flags=re.MULTILINE | re.IGNORECASE)
    
    # work_experiences = []
    # for i in range(1, len(parts), 2):
    #     # The header is the line with the date range
    #     header = parts[i]
    #     # The description is the text that came after it
    #     description = parts[i+1] if (i+1) < len(parts) else ""
        
    #     # Combine them into one block
    #     full_block = header + description
    #     work_experiences.append(full_block)
    
    # print(f"Found {len(work_experiences)} work experiences from the mixed-format text.\n")

    # for i, experience in enumerate(work_experiences):
    #     print(f"--- Experience Block {i+1} ---")
    #     print(experience.strip())
    #     print("\n")
        