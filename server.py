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
    "आलू": "Potato", "aalu": "Potato", "aloo": "Potato",
    "टमाटर": "Tomato", "tamatar": "Tomato",
    "प्याज": "Onion", "pyaz": "Onion",
}

STATE_MAP = {
    "kerala": "Keralam", "keralam": "Keralam",
    "up": "Uttar Pradesh", "uttar pradesh": "Uttar Pradesh",
    "mp": "Madhya Pradesh", "madhya pradesh": "Madhya Pradesh",
    "haryana": "Haryana", "punjab": "Punjab",
    "rajasthan": "Rajasthan", "maharashtra": "Maharashtra",
    "gujarat": "Gujarat", "bihar": "Bihar",
    "west bengal": "West Bengal", "karnataka": "Karnataka",
    "andhra pradesh": "Andhra Pradesh", "telangana": "Telangana",
    "tamil nadu": "Tamil Nadu", "tamilnadu": "Tamil Nadu",
}

FALLBACK_PRICES = {
    "Wheat": [{"mandi": "Karnal", "price": "2150", "date": "21/08/2026"}],
    "Paddy": [{"mandi": "Karnal", "price": "1950", "date": "21/08/2026"}],
    "Mustard": [{"mandi": "Hisar", "price": "5200", "date": "21/08/2026"}],
    "Potato": [{"mandi": "Agra", "price": "1200", "date": "21/08/2026"}],
    "Maize": [{"mandi": "Rohtak", "price": "1820", "date": "21/08/2026"}],
}

def fetch_live_prices(resolved_crop, resolved_state):
    url = "https://crop-price-proxy.anshul70503.workers.dev"

    params = {
        "crop": resolved_crop,
        "state": resolved_state
    }

    try:
        res = requests.get(url, params=params, timeout=10)

        if res.status_code == 200 and res.text.strip():
            data = res.json()
            records = data.get("records", [])

            if records:
                return [
                    {
                        "mandi": r.get("market", "Unknown"),
                        "price": r.get("modal_price", "N/A"),
                        "date": r.get("arrival_date", "N/A")
                    }
                    for r in records
                ]

    except Exception as e:
        print(f"Worker API error: {repr(e)}")

    return None

@app.get("/mandi-price")
def get_price(crop: str, state: str):
    resolved_crop = CROP_MAP.get(crop.strip(), None) or CROP_MAP.get(crop.strip().lower(), crop.title())
    resolved_state = STATE_MAP.get(state.strip().lower(), state.title())

    live = fetch_live_prices(resolved_crop, resolved_state)
    if live:
        return {
            "crop": resolved_crop,
            "state": resolved_state,
            "prices": live,
            "source": "live"
        }

    fallback = FALLBACK_PRICES.get(resolved_crop, [
        {"mandi": "Local Mandi", "price": "2000", "date": "21/08/2026"}
    ])
    return {
        "crop": resolved_crop,
        "state": resolved_state,
        "prices": fallback,
        "source": "fallback",
        "note": "Live data unavailable. Prices are indicative."
    }

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)