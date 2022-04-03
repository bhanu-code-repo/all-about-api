# Database Application

## How to use the project?
clone/download project and open folder in terminal and then run command `python .\app.py`

## About Project
Flask based application to access data from MySQL and MongoDB.

## Steps
1. Configure App
   * Request URL: http://localhost:port/configure-db
   * Request Body: {"username": "your username", "password": "your password", "conn-str": "your connection string"}
   * Request Type: POST
2. Get Database Data
   * Request URL: http://localhost:port/get-db-data
   * For SQL
     * Request Body: {"name": "fsds_course", "type": "SQL", "query": "SELECT * FROM FSDS_COURSE.STUDENTS"}
   * For MongoDB
     * Request Body: {"name": "bpst", "type": "MongoDB"} 
   * Request Type: POST