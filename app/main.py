from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Welcome to my Rest API",
        "Developer": "Reyhan Rafaidhil",
        "Reason" : "Project 2: HealthTech - Automated PHI/PII Redaction Pipeline for LLMs "
    }