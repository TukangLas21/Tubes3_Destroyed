import mysql.connector
import os

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
SQL_PATH = "data/applicant_data.sql"

class Connector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        
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
                
                ensure_db = self.ensure_database_exists()
                if ensure_db:
                    print("Database ensured and ready to use")
                    self.connection.database = self.database # make sure database is set
                else:
                    raise Exception("Failed to ensure database exists")
                
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
            
    def get_applicant_profile(self, applicant_id):
        if not self.connection or not self.connection.is_connected():
            print("No active connection")
            return None
        try:
            query = "SELECT * FROM ApplicantProfile WHERE applicant_id = %s"
            self.cursor.execute(query, (applicant_id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
    
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
        