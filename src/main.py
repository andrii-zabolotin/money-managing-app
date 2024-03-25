from fastapi import FastAPI

app = FastAPI(
    title="Money Managing App"
)


@app.get("/ping")
async def ping():
    return {"message": "pong"}
