import uvicorn
import os
from dotenv import load_dotenv
# Explicitly load before anything else
load_dotenv(override=True)

from app.main import app

if __name__ == "__main__":
    print(f"DIAGNOSTIC: GEMINI_API_KEY prefix: {os.environ.get('GEMINI_API_KEY', '')[:10]}...")
    uvicorn.run(app, host="127.0.0.1", port=8002)
