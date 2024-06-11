from pydantic import BaseModel
from typing import List

class Account(BaseModel): 
    balance : int
    account_no : int
    bank_code : int
class User(BaseModel):
    username: str
    hashedpassword: str
    accounts: List[Account]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
