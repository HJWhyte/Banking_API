import os
import logging
import pymongo
from config import CONNECTION_STRING

def db_connect():
    """Create DB connection client and access user collection"""
    logging.info(CONNECTION_STRING)
    try:
        # Create MongoClient obj
        client = pymongo.MongoClient(CONNECTION_STRING)
        # Connect to cluster
        db = client['BankAPI']
        # Assign collections
        users = db['users']
        # Return client and users db
        return client, users
    except pymongo.errors.ConfigurationError as e:
        return logging.error(f"DB connection failed: {e}")
        
    
def db_close(client):
    '''Closes DB connection'''
    client.close()
    return

