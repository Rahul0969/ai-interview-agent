from fastapi import FastAPI

app = FastAPI(title = "AI Interview Agent")

@app.get("/")
def root():
    return {"message": "AI Interview Agent is running"}