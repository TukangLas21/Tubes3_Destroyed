import os
import shutil

from faker import Faker

data_dir = './data'
output_file = './data/applicant_data.sql'
CV_PER_CATEGORY = 20
NUM_APPLICANTS = 100

fake = Faker('id_ID')
cv_paths = []

try:
    list_category = [
        folder for folder in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, folder))
    ]
    
    for category in list_category:
        category_path = os.path.join(data_dir, category)
        try:
            cv_path_in_folder = [
                file for file in os.listdir(category_path) if file.endswith('.pdf') and os.path.isfile(os.path.join(category_path, file))
            ]
            
            if not cv_path_in_folder:
                print(f"No CV files found in category '{category}'. Please ensure the directory contains PDF files.")
                exit()
                
            for file_name in cv_path_in_folder:
                cv_paths.append((category, file_name))    
    
        except FileNotFoundError:
            print(f"Category '{category}' does not exist in the data directory. Please ensure it contains subdirectories for each category.")
            exit()
        except Exception as e:
            print(f"An error occurred while processing category '{category}': {e}")
            exit()
except FileNotFoundError:
    print(f"Data directory '{data_dir}' not found. Please ensure it exists.")
    exit()   
except Exception as e:
    print(f"An error occurred while accessing the data directory: {e}")
    exit() 

print(f"Found categories: {len(list_category)}")
# print(list_category)
# exit()

# Create data using Faker
print("Generating applicant profiles...")
list_applicant_profile = []

for i in range (1, NUM_APPLICANTS + 1):
    first_name = fake.first_name().replace("'", "''")
    last_name = fake.last_name().replace("'", "''")
    address = fake.address().replace('\n', ', ').replace("'", "")
    phone_number = fake.phone_number().replace("'", "")
    
    applicant = {
        "applicant_id": i,
        "first_name": first_name,
        "last_name": last_name,
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=50).strftime('%Y-%m-%d'),
        "address": address,
        "phone_number": phone_number  
    }        
    list_applicant_profile.append(applicant)
    
command_applicant_profile = []

for profil in list_applicant_profile:
    first_name_sql = profil['first_name'].replace("'", "''")
    last_name_sql = profil['last_name'].replace("'", "''")
    address_sql = profil['address'].replace("'", "''")
    phone_number_sql = profil['phone_number'].replace("'", "''")
    command = f"INSERT INTO ApplicantProfile (applicant_id, first_name, last_name, date_of_birth, address, phone_number) VALUES ({profil['applicant_id']}, '{first_name_sql}', '{last_name_sql}', '{profil['date_of_birth']}', '{address_sql}', '{phone_number_sql}');"
    command_applicant_profile.append(command)

print(f"{len(command_applicant_profile)} applicant profiles generated.")

# Generate data for ApplicantDetail
print("Generating applicant details...")

command_applicant_detail = []
detail_id = 1

for idx, (category, file_name) in enumerate(cv_paths):
    applicant_id_for_cv = (idx % NUM_APPLICANTS) + 1
    applicant_role = category.replace("'", "''")
    
    # Path is saved relative to data directory (e.g. 'TEACHER/teacher1.pdf')
    path = f"{category}/{file_name}".replace("'", "''")
    
    command = f"INSERT INTO ApplicantDetail (detail_id, applicant_id, application_role, cv_path) VALUES ({detail_id}, {applicant_id_for_cv}, '{applicant_role}', '{path}');"
    command_applicant_detail.append(command)
    detail_id += 1
print(f"{len(command_applicant_detail)} applicant details generated.")

# Write to output file
print(f"Writing to output file '{output_file}'...")
try:
    with open(output_file, 'w') as f:
        for command in command_applicant_profile:
            f.write(command + '\n')
        for command in command_applicant_detail:
            f.write(command + '\n')
    print(f"Data successfully written to '{output_file}'.")
except Exception as e:
    print(f"An error occurred while writing to the output file: {e}")
    exit()
