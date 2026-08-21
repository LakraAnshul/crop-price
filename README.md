# Crop Price API

This is a FastAPI-based server that fetches crop prices from the Indian government's open data API.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   pip install fastapi uvicorn requests python-dotenv
   ```

2. Add your Data.gov.in API key to the `.env` file:
   ```env
   DATA_GOV_API_KEY=your_api_key_here
   ```

3. Run the server:
   ```bash
   uvicorn server:app --reload
   ```

## Usage

Access the API at:
`http://localhost:8000/mandi-price?crop=wheat&state=punjab`
