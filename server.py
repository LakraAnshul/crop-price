from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/mandi-price")
def get_price(crop: str, state: str):
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    params = {
        "api-key": os.getenv("DATA_GOV_API_KEY"),
        "format": "json",
        "filters[commodity]": crop,
        "filters[state]": state,
        "limit": 5
    }
    res = requests.get(url, params=params)
    data = res.json()
    records = data.get("records", [])
    return {"prices": [
        {
            "mandi": r["market"],
            "price": r["modal_price"],
            "date": r["arrival_date"]
        } for r in records
    ]}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)