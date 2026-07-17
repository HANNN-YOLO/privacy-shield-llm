from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "key" : "value",
        "message": "Welcome to my Rest API",
        "Developer": "Reyhan Rafaidhil",
        "Reason" : "Project 2: HealthTech - Automated PHI/PII Redaction Pipeline for LLMs",
        "HTTP Method" : "ini get"
    }

@app.post("/")
def root2():
    return{
        "key" : "value",
        "message": "Welcome to my Rest API",
        "Developer": "Reyhan Rafaidhil",
        "Reason" : "Project 2: HealthTech - Automated PHI/PII Redaction Pipeline for LLMs",
        "HTTP Method" : "ini post",
        "Status Code" : 200,
        "Announcement" : "Recived"
    }

@app.post("/redact")
def root3():
    return{
        "key" : "value",
        "message": "Welcome to my Rest API",
        "Developer": "Reyhan Rafaidhil",
        "Reason" : "Project 2: HealthTech - Automated PHI/PII Redaction Pipeline for LLMs",
        "HTTP Method" : "ini post di path redact",
        "Status Code" : 200,
        "Announcement" : "Recived"
    }