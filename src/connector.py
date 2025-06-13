import mysql.connector

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
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(True)
                print("Connection successful")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection = None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connection closed")
            
    def get_applicant_profile(self, detail_id):
        if not self.connection or not self.connection.is_connected():
            print("No active connection")
            return None
        try:
            query = "SELECT * FROM ApplicantProfile ap, ApplicantDetails ad WHERE ap.applicant_id = ad.applicant_id AND ad.detail_id = %s"
            self.cursor.execute(query, (detail_id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        
    
    
    
        
            
        