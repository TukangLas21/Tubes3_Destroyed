import mysql.connector
import os
from encryption import Encryption  

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
SQL_PATH = "data/applicant_data.sql"

class Connector:
    def __init__(self, host, user, password, database, encryption_key=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.encryption = Encryption(encryption_key) if encryption_key else None
        
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                auth_plugin='mysql_native_password'
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(True)
                print("Connection established successfully")
                
                # Check if database already exists
                self.cursor.execute("SHOW DATABASES")
                existing_databases = [db[0] for db in self.cursor.fetchall()]
                if self.database in existing_databases:
                    print(f"Database '{self.database}' already exists")
                    self.cursor.execute(f"USE {self.database}")
                    self.connection.database = self.database
                else:
                    raise ValueError(f"Database '{self.database}' does not exist. Please create it first.")
                
            else:
                print("Connection failed, no database specified")
                self.cursor = None
                
        except mysql.connector.Error as err:
            print(f"Error SQL: {err}")
            self.connection = None
            self.cursor = None
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.connection = None
            self.cursor = None
            
    # Create database if not exists and set up the data
    def ensure_database_exists(self):
        if not self.connection or not self.connection.is_connected():
            print("No active connection")
            return False
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.cursor.execute(f"USE {self.database}")
            
            sql_file_path = os.path.join(ROOT_DIR, SQL_PATH)
            
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                print(f"Executing SQL commands from {sql_file_path}")
                sql_commands = file.read().split(';')
                
            # Execute each command in the SQL file
            for command in sql_commands:
                if command.strip():
                    try:
                        self.cursor.execute(command)
                    except mysql.connector.Error as err:
                        print(f"Error executing command: {err}")
                            
            self.connection.commit()
            print("Database ensured and SQL commands executed")
            
            return True
        
        except mysql.connector.Error as err:
            print(f"Error in ensuring database: {err}")
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connection closed")
    
    # Gets all CV paths and their corresponding applicant IDs, saves in a dictionary
    def get_paths_applicantid(self):
        if not self.connection or not self.connection.is_connected():
            print("No active connection")
            return None
        
        try:
            query = "SELECT cv_path, applicant_id FROM ApplicationDetail"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return {cv_path: applicant_id for cv_path, applicant_id in results}
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        
    def encrypt_data(self):
        if not self.encryption or not self.connection or not self.connection.is_connected():
            print("No active connection or encryption not set")
            return False
        
        try:
            self.cursor.execute("SELECT applicant_id, first_name, last_name, address, phone_number FROM ApplicantProfile")
            applicants = self.cursor.fetchall()
            
            if not applicants:
                print("No applicants found to encrypt")
                return False
            
            print(f"Encrypting data for {len(applicants)} applicants")
            
            for profile in applicants:
                applicant_id, first_name, last_name, address, phone_number = profile
                
                encrypted_first_name = self.encryption.encrypt(first_name)
                encrypted_last_name = self.encryption.encrypt(last_name)
                encrypted_address = self.encryption.encrypt(address)
                encrypted_phone_number = self.encryption.encrypt(phone_number)
                
                update_query = """
                    UPDATE ApplicantProfile
                    SET first_name = %s, last_name = %s, address = %s, phone_number = %s
                    WHERE applicant_id = %s
                """
                
                self.cursor.execute(update_query, (
                    encrypted_first_name,
                    encrypted_last_name,
                    encrypted_address,
                    encrypted_phone_number,
                    applicant_id
                ))
                
            self.connection.commit()
            print("Data encryption completed successfully")
            return True
        except mysql.connector.Error as err:
            print(f"Error during encryption: {err}")
            return False
        except Exception as e:
            print(f"Unexpected error during encryption: {e}")
            return False
        
    def decrypt_data(self):
        if not self.encryption or not self.connection or not self.connection.is_connected():
            print("No active connection or encryption not set")
            return False
        
        try:
            self.cursor.execute("SELECT applicant_id, first_name, last_name, address, phone_number FROM ApplicantProfile")
            applicants = self.cursor.fetchall()
            
            if not applicants:
                print("No applicants found to encrypt")
                return False
            
            print(f"Decrypting data for {len(applicants)} applicants")
            
            for profile in applicants:
                applicant_id, first_name, last_name, address, phone_number = profile
                
                decrypted_first_name = self.encryption.decrypt(first_name)
                decrypted_last_name = self.encryption.decrypt(last_name)
                decrypted_address = self.encryption.decrypt(address)
                decrypted_phone_number = self.encryption.decrypt(phone_number)
                
                update_query = """
                    UPDATE ApplicantProfile
                    SET first_name = %s, last_name = %s, address = %s, phone_number = %s
                    WHERE applicant_id = %s
                """
                
                self.cursor.execute(update_query, (
                    decrypted_first_name,
                    decrypted_last_name,
                    decrypted_address,
                    decrypted_phone_number,
                    applicant_id
                ))
                
            self.connection.commit()
            print("Data decryption completed successfully")
            return True
        except mysql.connector.Error as err:
            print(f"Error during decryption: {err}")
            return False
        except Exception as e:
            print(f"Unexpected error during decryption: {e}")
            return False
        
    def get_decrypted_profile(self, applicant_id):
        if not self.encryption or not self.connection or not self.connection.is_connected():
            print("No active connection or encryption not set")
            return None
        
        try:
            query = "SELECT first_name, last_name, address, phone_number FROM ApplicantProfile WHERE applicant_id = %s"
            self.cursor.execute(query, (applicant_id,))
            profile = self.cursor.fetchone()
            
            if not profile:
                print(f"No profile found for applicant ID {applicant_id}")
                return None
            
            decrypted_profile = {
                'first_name': self.encryption.decrypt(profile[0]),
                'last_name': self.encryption.decrypt(profile[1]),
                'address': self.encryption.decrypt(profile[2]),
                'phone_number': self.encryption.decrypt(profile[3])
            }
            
            return decrypted_profile
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None