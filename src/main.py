import logging
import pymongo
from config import CONNECTION_STRING, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from auth import pwd_context,verify_password,create_jwt,authenticate_user ,get_current_user
from models import User, Account, Token, TokenData
from db import db_connect, db_close
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta, timezone


# Set Up Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI App
app = FastAPI()

@app.get("/")
def root():
    """Basic API route test"""
    return {"Test" : "API working!"}

@app.post("/createUser")
async def createUser(username: str, password: str):
    """Create user in DB"""
    logging.info(f"Username: {username}, Password: {password}")
    try:
        # Connect to DB and User Collection
        client, users = db_connect()
        # Hash the password
        hashedpassword = pwd_context.hash(password)
        # Create JSON User Obj
        userObj = jsonable_encoder(User(username=username, hashedpassword=hashedpassword, accounts=[]))
        logging.info(f"User Object : {userObj}")
        # Disallow duplicate usernames
        # users.create_index([("username", 1)], unique=True)
        # Add User to DB
        users.insert_one({username : userObj})
        logging.info("User successfully added")
        return("User successfully added")
    except pymongo.errors.DuplicateKeyError as e:
        logging.error(f"Duplicate user name, user creation failed. Error info: {e}")
        raise HTTPException(status_code=400, detail=f"Duplicate User, User Creation Failed")
    except pymongo.errors.PyMongoError as e:
        logging.error("DB connection failed")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    finally:
        db_close(client)

@app.post("/addAccount")
async def add_account(username: str, account_no: int, bank_code: int):
    """Add a bank account to a specific user"""
    logging.info(f"Username: {username}, Account No: {account_no}, Bank Code: {bank_code}")
    try:
        # Connect to DB and User Collection
        client, users = db_connect()
        # Check user exists
        if users.count_documents({username:{"$exists": True}}) == 0:
            raise HTTPException(status_code=404, detail=f"No user found: {username}")
        # Check for unique account num
        existing_account = users.find_one({username:{"$exists": True}, f"{username}.accounts.account_no": account_no})
        if existing_account:
            raise HTTPException(status_code=400, detail=f"Account: {account_no}, already exists for user: {username}")
        # Create account object
        accountObj = jsonable_encoder(Account(balance=0, account_no=account_no, bank_code=bank_code))
        # Add account to user
        users.update_one({username:{"$exists":True}}, {"$push":{f"{username}.accounts": accountObj}})
        logging.info(f"Account: {account_no} successfully added to {username}")
        return(f"Account: {account_no} successfully added to {username}")
    except pymongo.errors.PyMongoError as e:
        logging.error("DB connection failed")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
    finally:
        db_close(client)

@app.post("/deposit")
async def deposit(username: str, account_no: int, bank_code: int, amount: int):
    """Deposit into a users account"""
    logging.info(f"Username: {username}, Account No: {account_no}, Bank Code: {bank_code}, Amount : {amount}")
    try:
        # Connect to DB and User Collection
        client, users = db_connect()
        # Check user exists
        if users.count_documents({username:{'$exists': True}}) == 0:
            raise HTTPException(status_code=404, detail=f"No user found under {username}")
        # Define the filter to identify the document and the specific account
        filter_query = {
            f'{username}.accounts': {
                '$elemMatch': {
                    'account_no': account_no,
                    'bank_code': bank_code
                }
            }
        }
        # Update the correct accounts balance
        result = users.update_one(filter_query, {'$inc': {f'{username}.accounts.$.balance': amount}})
        # Check if the update was successful via number of documents updated
        if result.modified_count > 0:
            logging.info("Deposit Successful")
            return {"Deposit successful"}
        else:
            raise HTTPException(status_code=404, detail="No matching account found for the provided details.")
    except pymongo.errors.PyMongoError as e:
        logging.error("DB connection failed")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
    finally:
        db_close(client)

@app.post("/token", response_model=Token)
# Function depends on the necessary form data from request
async def access_token_login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    # Authenticate user with form data
    user_data = authenticate_user(username, password)
    if not user_data:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    # Create a bearer token with the subject being the username
    token_data = {"sub":username}
    return {"access_token": create_jwt(token_data), "token_type": "bearer"}

@app.get("/balance")
async def get_balance(current_user: TokenData = Depends(get_current_user)):
    """Function to allow the authorized user to view their accounts and balances"""
    # Get the authorized users username
    username = current_user.username
    # Connect to DB and get collection
    client, users = db_connect()
    try:
        # Find the user document based on the username
        user_data = users.find_one({username: {"$exists": True}})
        if not user_data:
            raise HTTPException(status_code=404, detail=f"User {username} not found")
        # Get the users account details, if none default an empty list
        accounts = user_data[username].get("accounts", [])
        return {"accounts": accounts}
    except pymongo.errors.PyMongoError as e:
        logging.error("DB connection failed")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
    finally:
        db_close(client)

