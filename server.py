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
    "आलू": "Potato", "aalu": "Potato", "aloo": "Potato",
    "टमाटर": "Tomato", "tamatar": "Tomato",
    "प्याज": "Onion", "pyaz": "Onion",
}

FALLBACK_PRICES = {
    "Wheat": [{"mandi": "Karnal", "price": "2150", "date": "21/08/2026"}],
    "Paddy": [{"mandi": "Karnal", "price": "1950", "date": "21/08/2026"}],
    "Mustard": [{"mandi": "Hisar", "price": "5200", "date": "21/08/2026"}],
}

@app.get("/mandi-price")
def get_price(crop: str, state: str):
    resolved_crop = CROP_MAP.get(crop.strip(), None) or CROP_MAP.get(crop.strip().lower(), crop.title())

    api_key = os.getenv("DATA_GOV_API_KEY", "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b")

    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    params = {
        "api-key": api_key,
        "format": "json",
        "filters[state.keyword]": state.title(),
        "filters[commodity]": resolved_crop,
        "limit": 5
    }

    try:
        res = requests.get(url, params=params, timeout=15)
        if res.status_code == 200 and res.text.strip():
            data = res.json()
            records = data.get("records", [])
            if records:
                return {
                    "crop": resolved_crop,
                    "state": state,
                    "prices": [
                        {
                            "mandi": r.get("market", "Unknown"),
                            "price": r.get("modal_price", "N/A"),
                            "date": r.get("arrival_date", "N/A")
                        } for r in records
                    ],
                    "source": "live"
                }
    except Exception:
        pass

    # Fallback if API fails or returns empty
    fallback = FALLBACK_PRICES.get(resolved_crop, [
        {"mandi": "Local Mandi", "price": "2000", "date": "21/08/2026"}
    ])
    return {
        "crop": resolved_crop,
        "state": state,
        "prices": fallback,
        "source": "fallback",
        "note": "Live data unavailable. Prices are indicative."
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)