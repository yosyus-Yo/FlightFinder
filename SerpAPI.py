
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def search_google_flights(departure_id, arrival_id, outbound_date, hl="en", currency="USD", outbound_times="0,23", max_price=None):
    api_key = os.getenv("SERPAPI_KEY")
    base_url = "https://serpapi.com/search"
    parameters = {
        "engine": "google_flights",
        "type": "2",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "hl": hl,
        "currency": currency,
        "outbound_times": outbound_times,
        "max_price": max_price,
        "api_key": api_key
    }
    response = requests.get(base_url, params=parameters)
    if 'best_flights' in response.json():
        return response.json()['best_flights']
    else :
        print("No 'best_flights' key in response. Response:", response)
        return None
    

# Function to search for flights on specific dates
def search_flights(departure_id, arrival_id, outbound_date, return_date = None, hl = "ko", currency = "KRW", outbound_times = "0,23", return_times = "0,23", max_price = None):
    outbound_flights = search_google_flights(departure_id, arrival_id, outbound_date, hl=hl, currency=currency, outbound_times=outbound_times)
    if return_date != None:
        inbound_flights = search_google_flights(departure_id = arrival_id, arrival_id = departure_id, outbound_date = return_date, hl=hl, currency=currency, outbound_times = return_times)
        return {"outbound_flights": outbound_flights, "inbound_flights": inbound_flights}
    return {"outbound_flights": outbound_flights}