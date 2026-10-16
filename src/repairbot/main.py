import uvicorn


def main():
    uvicorn.run("src.repairbot.api.http_api:app", host="0.0.0.0", port=80, reload=True)
