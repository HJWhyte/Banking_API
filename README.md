**FastAPI Banking API**
This is a simple FastAPI-based API for basic banking operations. 
It includes functionality for user registration, adding bank accounts, depositing funds, and checking account balances.

*** SEE BOTTOM OF DOCUMENT FOR ERRORS/INCOMPLETION ***

**How to use:**

To run locally: 
  
- Ensure all required environmental variables are available 
- Ensure you are within the src directory
- Start Python Virtual Environment 
- Install requirements.txt within venv
- Run 'uvicorn main:app --reload'

**To run via Docker:**

- Ensure all required environmental variables are available, within .env file
- Ensure you are within the src directory
- Run 'docker build -t <insertname> .' 
- Run 'docker run --env-file .env -p 8000:8000 <insertname>' 

**Features**

**User Registration (/createUser):**
Endpoint to create a new user in the database.
Requires a unique username and a password.
Passwords are hashed before storage.

**Add Bank Account (/addAccount):**
Adds a bank account to a specific user.
Checks for the existence of the user and ensures account uniqueness.
Accounts include a balance, account number, and bank code.

**Deposit Funds (/deposit):**
Deposits funds into a user's account.
Validates user existence and account details.
Updates the account balance.

**Get Access Token (/token):**
Retrieves a bearer token for authentication.
Requires a valid username and password.

**Get Account Balances (/balance):**
Allows an authorized user to view their accounts and balances.
Requires a valid bearer token for authentication.

*** ERROR/INCOMPLETION ***

- Due to some initially poor data modelling choices, there is a DB error which only allows one document to be uploaded to the Mongo Cluster - This error only came up at the point 2 attempt task 1.2 as it requires a 2nd user to transfer to/from. Due to the time constraints of the task I decided it would be better to priotize other aspects of the task than continue debugging, therefore tasks 1.2 and 1.3 were not able to be included within the timelimit. I believe thet underlying logic would of been fairly simple and would be more than happy to explain how I would of approached said tasks/


