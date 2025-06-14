import fitz
import os

src_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(src_dir)

def extract_text(file_path):
    
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
    
    
        