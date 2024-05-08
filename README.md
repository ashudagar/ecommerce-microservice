# ecommerce-microservice
Micro Services design for an ecommerce project

This project has 3 microservices as auth, order and product running on 5000, 5001, 5002 port respectively.

## Setup
1. Clone the project
2. Create a virtual env - 'python3 -m venv ecomm-env'
3. Activate virtual env - 'source ecomm-env/bin/activate'
4. Install dependencies - 'pip install -r auth_ms/requirements.txt'
5. Run all microservices - 
   6. 'python auth_ms/app.py'
   7. 'python order_ms/app.py'
   8. python product_ms/app.py

## Sample Curl Requests
Following file has the Postman Collections in the same directory

            [Ecommerce-microservice API requests.postman_collection.json](Ecommerce-microservice%20API%20requests.postman_collection.json)
