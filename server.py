from fastapi import FastAPI
import requests
import os

app = FastAPI()

CROP_MAP = {
    "गेहूँ": "Wheat", "गेहू": "Wheat", "gehu": "Wheat", "gehun": "Wheat",
    "धान": "Paddy", "dhan": "Paddy", "chawal": "Paddy",
    "मक्का": "Maize", "makka": "Maize",
    "सोयाबीन": "Soybean", "soyabean": "Soybean",
    "सरसों": "Mustard", "sarson": "Mustard",
    "चना": "Gram", "chana": "Gram",
    "बाजरा": "Bajra", "bajra": "Bajra",
}

# Hardcoded realistic fallback prices for demo
FALLBACK_PRICES = {
    "Wheat": [
        {"mandi": "Karnal", "price": "2150", "date": "21/08/2026"},
        {"mandi": "Panipat", "price": "2130", "date": "21/08/2026"},
        {"mandi": "Ambala", "price": "2160", "date": "21/08/2026"},
    ],
    "Paddy": [
        {"mandi": "Karnal", "price": "1950", "date": "21/08/2026"},
        {"mandi": "Kurukshetra", "price": "1920", "date": "21/08/2026"},
        {"mandi": "Kaithal", "price": "1970", "date": "21/08/2026"},
    ],
    "Maize": [
        {"mandi": "Rohtak", "price": "1820", "date": "21/08/2026"},
        {"mandi": "Hisar", "price": "1800", "date": "21/08/2026"},
        {"mandi": "Sirsa", "price": "1840", "date": "21/08/2026"},
    ],
    "Mustard": [
        {"mandi": "Hisar", "price": "5200", "date": "21/08/2026"},
        {"mandi": "Bhiwani", "price": "5180", "date": "21/08/2026"},
        {"mandi": "Fatehabad", "price": "5220", "date": "21/08/2026"},
    ],
    "Gram": [
        {"mandi": "Hisar", "price": "4800", "date": "21/08/2026"},
        {"mandi": "Sirsa", "price": "4750", "date": "21/08/2026"},
        {"mandi": "Fatehabad", "price": "4820", "date": "21/08/2026"},
    ],
}

@app.get("/mandi-price")
def get_price(crop: str, state: str):
    resolved_crop = CROP_MAP.get(crop.strip(), None)
    if not resolved_crop:
        resolved_crop = CROP_MAP.get(crop.strip().lower(), crop.title())

    prices = FALLBACK_PRICES.get(resolved_crop, [
        {"mandi": "Local Mandi", "price": "2000", "date": "21/08/2026"}
    ])

    return {
        "crop": resolved_crop,
        "state": state,
        "prices": prices,
        "note": "Prices are indicative. Confirm at mandi gate on arrival."
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)