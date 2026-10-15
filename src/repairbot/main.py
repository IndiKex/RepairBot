import os

import uvicorn
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv("secrets.env")
    secret_key = os.environ["AUTHENTICATION_KEY"]
    print(secret_key)

    uvicorn.run("api.experiment.api:app", host="0.0.0.0", port=80, reload=True)
