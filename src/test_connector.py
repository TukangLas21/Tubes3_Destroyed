from connector import Connector

"""
Test script for Connector class, integrate this later
"""
def test_connector(host, user, password, database):
    connector = Connector(host, user, password, database)
    
    # Test connection
    connector.connect()
    if connector.connection is None:
        raise Exception("Connection failed")
    
    # Test fetching applicant profile
    detail_id = 1  
    profile = connector.get_applicant_profile(detail_id)
    if profile is None:
        raise Exception("Failed to fetch applicant profile")
    
    # Test closing connection
    connector.close()
    if connector.connection is not None and connector.connection.is_connected():
        raise Exception("Connection was not closed properly")
    
    print("All tests passed, connection ready to be used.")
    return connector


if __name__ == "__main__":
    # Replace with your actual database credentials
    host = input("Enter database host: ")
    user = input("Enter database user: ")
    password = input("Enter database password: ")
    database = input("Enter database name: ")
    try:
        connector = test_connector(host, user, password, database)
    except Exception as e:
        print(f"Test failed: {e}")
    else:
        print("Connector is ready for use.")
    
    