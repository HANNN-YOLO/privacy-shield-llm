So now I want to build an API Test and see what happened over the course of 1 week.

For API Testing

Testing for the Fast API Server, I tested the GET, POST, and POST /name_path endpoints until they were successful. If you want to see proof, you can access my 📂 images folder. Up to 📂Week 1 Day 3, I only tested if I used localhost and IPv4, and it worked. So next I'll try the Endpoint for Using the Front-End UI to the Fast API Back-End. So if you want to see my proof, you can access it from the 📂 images folder until 📂Week 1 Day 7 - Front-End to Back-End Integration. I created a folder for 📂IPv4 and 📂 for HTTP Methods using only GET and POST. So I want to tell you in my proof for Front-End to Back-End Integration, I only see the status of the Fast API for GET, because my logic from the Front-End is only using app.js to call the function. from api.js, in api.js using condition so that if api.js can access back-end then the status is success and call the function again from ui.js to refresh the UI page. Next, if you see my proof for Front-End and Back-End Integration, I just explain how the integration from Front-End to Back-end is only for POST, so from Front-End has app.js logic to call api.js function for connection to Back-end using main.py, in main.py call redact.py function from route folder, so in /route/redact.py call function from schema folder using request.py and response.py sequentially, so back again to /route/redact.py in my code I just call redact_service.py function, and in the process redact_service.py function call validator.py again, so if from Back-End everything is successful then Front-End just give response from api.js function, in api.js call ui.js function So, refresh the page if get edited result.

JSON Validation, so I tested JSON Validation to check for Invalid Data Type, Invalid JSON, Missing Columns, and Null Values. You can see my proof from the 📂 image to 📂 week 1 day 5 - Error Handling. And if you want to understand it, I have proof only from the back-end in week 1 day 5 - Error Handling and 📂 Week 1 Day 7 - Front-End to Back-End Integration to 📂 Error Handling. The only difference is, if I only use the Back-End, I can get error handling documentation from the Fast API for Invalid Data Type, Invalid JSON, and Missing Columns and manual error handling for Null Values. If I try to integrate the Front-End to the Back-End, I only get a notification from the Front-End if I edit a Null Value.

API documentation if you want to access my proof for image formats, so you can follow this
privacy-shield-llm/
├── Back-End/
│ ├── app/
│ └── venv/
├── Doc/
│ ├── week 1/
│ └── week 2/
├── Front-End/
│ ├── css/
│ └── js/
│ └── index.html
├── images/
│ ├── Week 1 Day 3 - Get & Post/
│ ├── Week 1 Day 5 - Error Handling/
│ └── Week 1 Day 7 - Front-End to Back-End Integration
└── README.md

For Week 1 as Member 1
So, my document for 1 week, on Day 1 I learned API Concepts, HTTP Methods, Request & Response, JSON, Fast API. On Day 2 I will build a Fast API initialization for a Modular Project so this project can be scaled in the future. On Day 3 I will build GET, POST, POST /path_name endpoints using only the Back-End so I can see my proof in the 📂 images folder. 📂 Week 1 Day 3 - Get & Post. On Day 4 I used pydantic from the Python library, so I know what request & response validation and JSON parsing are. On Day 5 I will try Error Handling only on the Back-End using Postman to test GET and POST endpoints, so in Handling My mistakes: Find out if manual error handling is only for null values, if from Fast API it only gives documentation errors such as incorrect data types, JSON validation, and missing fields. On day 6 I will build the front-end UI, refactor the back-end and connect the front-end to the back-end using CORS, and on the last day I will document for 1 week.
