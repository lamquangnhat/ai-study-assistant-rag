from fastapi import FastAPI

app = FastAPI(
    title="StudyMate AI",
    description="AI Study Assistant using Retrieval-Augmented Generation",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "StudyMate AI is ready to learn!",
        "version": "0.1.0",
    }