import requests
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

POSITIONSTACK_API_KEY = os.getenv('API_KEY')  
BASE_URL = "http://api.positionstack.com/v1/forward"
csv_file_path = './sachse.csv'
result_file_path = './updated_dallas_addresses.csv'

def geocode_address(address):
    params = {'access_key': POSITIONSTACK_API_KEY, 'query': address}
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json().get('data', [])

def get_best_results(data):
    if not data:
        return []
    highest_confidence = max(item.get('confidence', 0) for item in data)
    return [item for item in data if item.get('confidence', 0) == highest_confidence]

def format_address_result(result):
    latitude = result.get('latitude', 'N/A')
    longitude = result.get('longitude', 'N/A')
    confidence = result.get('confidence', 0)
    label = result.get('label', 'N/A')
    return f"Address: {label} (Latitude: {latitude}, Longitude: {longitude}), Confidence: {confidence}"

def check_addresses(file_path):
    df = pd.read_csv(file_path)
    if "address" not in df.columns:
        raise ValueError("CSV file must contain an 'address' column")
    df["actual_address"] = ""
    for idx, address in df["address"].dropna().items():
        if not address.strip():
            df.at[idx, "actual_address"] = "Invalid or missing"
            continue
        try:
            response_data = geocode_address(f"{address}, dallas, TX, USA")
            best_results = get_best_results(response_data)
            if best_results:
                actual_addresses = [format_address_result(result) for result in best_results]
                df.at[idx, "actual_address"] = str(actual_addresses)
            else:  
                df.at[idx, "actual_address"] = "Could not be geocoded"
        except requests.RequestException as e:
            df.at[idx, "actual_address"] = f"Error: {e}"

    df.to_csv(result_file_path, index=False)
    print(f"Updated addresses have been written to {result_file_path}")

if __name__ == "__main__":
    check_addresses(csv_file_path)
