This is all document shows all Docker-related commands for team: CS5500BSY 

1. Package requirements:
pip install -r requirements.txt

2. Build the Docker Image:
docker build -t myimage .

3. Start the Docker Container
docker run -d --name mycontainer -p 80:80 myimage

4. How to call API:

Authentication Endpoints
1. User Signup
Endpoint: /api/signup
Method: POST
Description: Registers a new user.
Request Body Example:

{
  "email": "johndoe@example.com",
  "password": "password123",
  "username": "john_doe",
  "role": "user"
}
Response Example:

{
  "message": "User created successfully",
  "user_id": 1
}
2. User Login
Endpoint: /api/login
Method: POST
Description: Authenticates a user and returns an access token.
Request Body Example:

{
  "email": "johndoe@example.com",
  "password": "password123"
}
Response Example:

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer"
}
Admin Endpoints
1. Read All Users (Admin only)
Endpoint: /admin/users
Method: GET
Description: Retrieves all registered users. Accessible only to admin users.
Response Example:

[
  {
    "id": 1,
    "email": "johndoe@example.com",
    ...
  },
  ...
]
Payment Endpoints
1. Get All Transactions
Endpoint: /api/transactions
Method: GET
Description: Retrieves all transactions made by the authenticated user.
Query Parameters:
start_time: Start date (optional).
end_time: End date (optional).
Response Example:

[
  {
    "id": 1,
    "business_id": 101,
    "amount": 200.00,
    ...
  },
  ...
]
2. Get Specific Transaction
Endpoint: /api/transaction/{transaction_id}
Method: GET
Description: Retrieves details of a specific transaction.
Path Parameters:
transaction_id: ID of the transaction.
Response Example:

{
  "id": 1,
  "business_id": 101,
  "amount": 200.00,
  ...
}
3. Create a Transaction
Endpoint: /api/transaction
Method: POST
Description: Creates a new transaction.
Request Body Example:

{
  "business_id": 101,
  "card_number": "123456789012",
  "card_type": 0,
  "amount": 100.00,
  "description": "Purchase at Business 101"
}
Response Example:

{
  "id": 2,
  "user_id": 1,
  "business_id": 101,
  "type": 0,
  "status": "completed",
  "amount": 100.00,
  ...
}