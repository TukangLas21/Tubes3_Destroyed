import mysql.connector

def update_cv_paths_in_database(database_name, user="root", password="your_password"):
    """
    Updates CV paths by prepending 'data/' to existing paths in the database
    """
    try:
        # Connect to database
        cnx = mysql.connector.connect(
            user=user,
            password=password,
            host="localhost",
            database=database_name,
            auth_plugin="mysql_native_password"
        )
        cursor = cnx.cursor()
        
        # First, get all records to see what we're updating
        cursor.execute("SELECT detail_id, cv_path FROM ApplicationDetail")
        records = cursor.fetchall()
        
        print(f"Found {len(records)} records to update")
        
        # Update records that don't already start with "data/"
        update_count = 0
        for detail_id, cv_path in records:
            if not cv_path.startswith("data/"):
                new_path = f"data/{cv_path}"
                update_query = "UPDATE ApplicationDetail SET cv_path = %s WHERE detail_id = %s"
                cursor.execute(update_query, (new_path, detail_id))
                update_count += 1
                
        # Commit the changes
        cnx.commit()
        
        print(f"Successfully updated {update_count} CV paths")
        
        cursor.close()
        cnx.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False

def main():
    database_name = input("Enter database name: ")
    password = input("Enter database password: ")
    
    if update_cv_paths_in_database(database_name, password=password):
        print("CV path update completed successfully")
    else:
        print("Failed to update CV paths")

if __name__ == "__main__":
    main()