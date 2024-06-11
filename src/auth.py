from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from db import db_connect, db_close
from models import TokenData

# Initialize password hashing concept
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize Oauth2 password authentication flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    """Compare entered password with hashedpassword"""
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt(data: dict):
    """Create a Java Web Token with expiration date"""
    # Copy the data to be tokenized 
    to_encode = data.copy()
    # Calculate token expiration and add to data
    expires = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expires})
    # Create and return JWT
    jwtoken = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return jwtoken

def authenticate_user(username:str, password: str):
    """Authenticate that a user exists in the DB and passwords match"""
    # Connect to DB and Collection
    client, users = db_connect()
    # Check user exists
    if users.count_documents({username:{'$exists': True}}) == 0:
        return False
    # Find stored user data
    user_data = users.find_one({username:{'$exists': True}})
    # Verify the passwords match
    if not verify_password(password, user_data[username]['hashedpassword']):
        return False
    # If successful, close DB connection and return user data
    db_close(client)
    return user_data

def get_current_user(token: str = Depends (oauth2_scheme)):
    """Extract the and validate the current user's JWT token"""
    # Create exception if credentials fail
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        # Decode token
        token_payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        # Get username from token subject
        username: str = token_payload.get("sub")
        if username is None:
            raise credentials_exception
        # Create and return token data model containing current user's username 
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception