1. Base Url : http://35.166.135.167
2. Bug report git link : https://github.com/cs5500BSY/opp-api/issues

3. Example commands : 

**User SignUp**
curl -X POST http://35.166.135.167/api/signup \
-H "Content-Type: application/json" \
-d '{"email": "CS5500BSY@neu.edu", "password": "yourpassword", "username": "newuser", "role": "user"}'
**User Login**
curl -X POST http://35.166.135.167/api/login \
-H "Content-Type: application/json" \
-d '{"email": "CS5500BSY@neu.edu", "password": "yourpassword"}'
**Get All Users (Admin only)**
curl -X GET http://35.166.135.167/admin/users \
-H "Authorization: Bearer YourAccessToken"
**Create a Transaction**
curl -X POST http://35.166.135.167/api/transaction \
-H "Content-Type: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QHRlc3QuY29tIiwiaWQiOjMsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwMTkzMzAzN30.e8wNp6kltlIPN7JN3ovK28F7SlH1xQves9luywBWOyA" \
-d '{"business_id": 1, "card_number": "123456789012", "card_type": 0, "amount": 100.00, "description": "Purchase at Business 1"}'
**Get All Transactions**
curl -X GET "http://35.166.135.167/api/transactions" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QHRlc3QuY29tIiwiaWQiOjMsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwMTkzMzAzN30.e8wNp6kltlIPN7JN3ovK28F7SlH1xQves9luywBWOyA"
**Get Specific Transaction**
curl -X GET http://35.166.135.167/api/transaction/1 \
-H "Authorization: Bearer YourAccessToken"
**Create a Business**
curl -X POST http://35.166.135.167/api/business \
-H "Content-Type: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QHRlc3QuY29tIiwiaWQiOjMsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwMTkzMzAzN30.e8wNp6kltlIPN7JN3ovK28F7SlH1xQves9luywBWOyA" \
-d '{"name": "Business Name", "description": "Business Description"}'
**Get Specific Business Details**
curl -X GET http://35.166.135.167/api/business/1 \
-H "Authorization: Bearer YourAccessToken"

