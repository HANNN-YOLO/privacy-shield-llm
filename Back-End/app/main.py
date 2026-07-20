from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.redact import router as redact_router

app = FastAPI(
    title="Privacy Shield LLM API",
    version="1.0.0"
)

# ==========================================
# CORS Configuration
# ==========================================

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://10.234.155.226:5500",

    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://10.234.155.226:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# Router
# ==========================================
app.include_router(redact_router)


# ==========================================
# Health Check
# ==========================================
@app.get("/")
def root():
    return {
        "application": "Privacy Shield LLM",
        "status": "Running",
        "version": "0.5.0"
    }