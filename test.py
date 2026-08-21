from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

CROP_MAP = {
    "गेहूँ": "Wheat", "गेहू": "Wheat", "gehu": "Wheat", "gehun": "Wheat",
    "धान": "Paddy", "dhan": "Paddy", "chawal": "Paddy",
    "मक्का": "Maize", "makka": "Maize",
    "सोयाबीन": "Soybean", "soyabean": "Soybean",
    "सरसों": "Mustard", "sarson": "Mustard",
    "चना": "Gram", "chana": "Gram",
    "बाजरा": "Bajra", "bajra": "Bajra",
    "कपास": "Cotton", "kapas": "Cotton",
    "गन्ना": "Sugarcane", "ganna": "Sugarcane",
}

@app.get("/mandi-price")
def get_price(crop: str, state: str):
    resolved_crop = CROP_MAP.get(crop.strip().lower(), crop)
    resolved_crop = CROP_MAP.get(crop.strip(), resolved_crop)

    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    params = {
        "api-key": os.getenv("DATA_GOV_API_KEY", "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"),
        "format": "json",
        "filters[state.keyword]": state.title(),
        "filters[commodity]": resolved_crop,
        "limit": 5
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code != 200 or not res.text.strip():
            return {"prices": [], "error": f"API returned status {res.status_code}"}
        data = res.json()
        records = data.get("records", [])
        return {"prices": [
            {
                "mandi": r.get("market", "Unknown"),
                "price": r.get("modal_price", "N/A"),
                "date": r.get("arrival_date", "N/A")
            } for r in records
        ]}
    except Exception as e:
        return {"prices": [], "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)