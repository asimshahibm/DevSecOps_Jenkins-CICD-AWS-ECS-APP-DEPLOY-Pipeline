import os

from fastapi import FastAPI

app = FastAPI(
    title="DevSecOps ECS Sample",
    version=os.getenv("APP_VERSION", "local"),
    description="Sample application deployed through GitHub Actions or Jenkins.",
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "DevSecOps ECS Sample is running."}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "environment": os.getenv("APP_ENV", "local")}
