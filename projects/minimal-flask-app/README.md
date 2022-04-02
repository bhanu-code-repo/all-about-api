# Minimal Flask App

## How to use the project?
clone/download project and open folder in terminal and then run command `python .\app.py`

## About Project
Minimal Flask App with `GET` and `POST` routes to perform basic mathematical operatons i.e. addition, subtraction, multiplication and division for two numbers passed inside request body

For `GET` request,
* Request URL: http://localhost:9000/compute
* Set Request Type: GET

For `POST` request,
* Request URL: http://localhost:9000/compute
* Set Request Type: POST
* Set Request Header, `Content-Type` as `application/json`
* Request Body: `{"num1": 5, "num2": 5, "operation": "multiply"}`
* note: `operation` values can be one out of `add, subtract, divide, multiply`