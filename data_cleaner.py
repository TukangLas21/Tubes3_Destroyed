import os
import shutil

dataset_path = "./dataset"
data_path = "./data"

file_per_category = 20

try:
    category_list = [
        folder for folder in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, folder))
    ]
except FileNotFoundError:
    print(f"Dataset path '{dataset_path}' does not exist.")
    exit()
    
for category in category_list:
    category_path = os.path.join(dataset_path, category)
    print(f"Processing {category} category...")
    
    try:
        file_in_category = [
            file for file in os.listdir(category_path) if file.lower().endswith(".pdf")
        ]
        
        file_in_category.sort()
        
        chosen_files = file_in_category[:file_per_category]
        
        if not chosen_files:
            print(f"No PDF files found in category '{category}'. Skipping...")
            continue
        
        print(f"Found {len(file_in_category)} PDF files, choosing {len(chosen_files)} files.")
        
        data_category_path = os.path.join(data_path, category)
        os.makedirs(data_category_path, exist_ok=True)
        
        for file in chosen_files:
            src_path = os.path.join(category_path, file)
            dest_path = os.path.join(data_category_path, file)
            try:
                shutil.copy(src_path, dest_path)
                print(f"Copied {file} to {data_category_path}.")
            except Exception as e:
                print(f"Error copying {file}: {e}")
        
        print(f"Finished processing {category} category.\n")
    except FileNotFoundError:
        print(f"Category path '{category_path}' does not exist. Skipping category '{category}'.")
    except Exception as e:
        print(f"An error occurred while processing category '{category}': {e}")
        
print("Data cleaning completed.")
        