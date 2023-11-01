```
POST /api/user/signup
request body: 
{
    email:"sdfsdf",
    password:"sdfsdfsd"
}
response header: 201

```

```
POST /api/user/login
request body: 
{
    email:"sdfsdf",
    password:"sdfsdfsd"
}

response header: 200
response body: 
{
    user_id:"sdfsd",
    jwt_token:"dsfsdf"
}

response header: 401
response body: 
{
    message:"Unauthorized"
}

```
```
POST /api/pay?card_type=
header: Authorization: 'Bearer token'
request body: 
{
    card_number:"sdfsdf",
    amount:"2374.30",
    business_id:"sdfsddfsd",
    info:{
        xxx:dsddd,
        sss:sdfds
    },
    password:"sdfsdfsd"
}

response header: 200
response body: 
{
    message:"success"
}

response header: 400
response body: 
{
    message:"failed",
    reson:"dsfsdf"
}

```

Other common GET APIs:
```
GET /api/transaction?transaction_id=&start_time=&end_time=

GET /api/balance?start_time=&end_time=

GET /api/pending?start_time=&end_time=
```