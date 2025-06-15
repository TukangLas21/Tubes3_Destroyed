import mysql.connector
from encryption import Encryption  

class Connector:
    _instance = None
    _initialized = False
    
    def __new__(cls, host=None, user=None, password=None, database=None, encryption_key=None):
        if cls._instance is None:
            cls._instance = super(Connector, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, host=None, user=None, password=None, database=None, encryption_key=None):
        # Only initialize once
        if not self._initialized:
            if not all([host, user, password, database]):
                raise ValueError("All connection parameters (host, user, password, database) must be provided for first initialization")
            
            self.host = host
            self.user = user
            self.password = password
            self.database = database
            self.connection = None
            self.cursor = None
            self.encryption = Encryption(encryption_key) if encryption_key else None
            self._initialized = True
        else:
            # If already initialized, optionally update encryption key if provided
            if encryption_key is not None:
                self.encryption = Encryption(encryption_key)
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("Connector instance not created yet. Use Connector(host, user, password, database) first.")
        return cls._instance
    
    @classmethod
    def is_initialized(cls):
        return cls._instance is not None and cls._instance._initialized
    
    @classmethod
    def reset_instance(cls):
        if cls._instance:
            cls._instance.close()
        cls._instance = None
        cls._initialized = False
        
    def connect(self):
        if self.connection and self.connection.is_connected():
            print("Already connected to the database")
            return
        
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
                self.cursor.close() if self.cursor else None
                self.connection.close() if self.connection else None
                
        except mysql.connector.Error as err:
            print(f"Error SQL: {err}")
            self.connection.close() if self.connection else None
            self.cursor.close() if self.cursor else None
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.connection.close() if self.connection else None
            self.cursor.close() if self.cursor else None
            
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connection closed")
    
    # Gets all CV paths and their corresponding applicant IDs, saves in a dictionary
    def get_paths_id(self):
        if not self.connection or not self.connection.is_connected():
            print("No active connection")
            return None
        
        try:
            query = "SELECT detail_id, applicant_id, cv_path FROM ApplicationDetail"
            self.cursor.execute(query)
            return self.cursor.fetchall()
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
                print("No applicants found to decrypt")
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


# Example usage:
if __name__ == "__main__":
    # First initialization - creates the singleton instance
    db1 = Connector("localhost", "root", "password", "mydb", "encryption_key")
    
    # Subsequent calls return the same instance
    db2 = Connector()  # Parameters are ignored since instance already exists
    
    # Both variables reference the same instance
    print(db1 is db2)  # True
    
    # Alternative way to get the instance
    db3 = Connector.get_instance()
    print(db1 is db3)  # True
    
    # Connect and use the database
    db1.connect()
    
    # Reset instance if needed (for testing or changing connection parameters)
    # Connector.reset_instance()
    # new_db = Connector("new_host", "new_user", "new_pass", "new_db")