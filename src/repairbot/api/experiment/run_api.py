import uvicorn


def main():
    uvicorn.run(
        "src.repairbot.api.experiment.api:app", host="0.0.0.0", port=80, reload=True
    )
