from fastapi import FastAPI
from routers import ai, skills, jobs

app = FastAPI(
    title="LinkedInsight",
    description="AI-powered career & skills navigator",
    version="0.1.0",
)

# Register routers
app.include_router(ai.router)
app.include_router(skills.router)
app.include_router(jobs.router)

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# TODO: add middleware, logging, and error handling later

