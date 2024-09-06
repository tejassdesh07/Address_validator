from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Replace with your Google Maps API key
GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'

class Address(BaseModel):
    address: str

@app.post("/validate-address/")
async def validate_address(address: Address):
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    
    # Set up parameters for the request
    params = {
        'address': address.address,
        'key': GOOGLE_MAPS_API_KEY
    }
    
    # Send the request to Google Maps API
    response = requests.get(geocode_url, params=params)
    
    # Check the status code of the response
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error contacting Google Maps API")
    
    # Process the JSON response
    try:
        data = response.json()
        if data['status'] == 'OK':
            # Return the first result if available
            return {"google_maps_response": data['results'][0]}
        else:
            raise HTTPException(status_code=400, detail=f"Google Maps API error: {data['status']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing Google Maps response: {e}")




# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import requests

# app = FastAPI()

# # Replace with your USPS Web Tools API credentials
# USPS_USER_ID = '03S811AGILE29'  

# class Address(BaseModel):
#     address: str

# @app.post("/validate-address/")
# async def validate_address(address: Address):
#     usps_api_url = "https://secure.shippingapis.com/ShippingAPI.dll"
    
#     # Prepare the XML request
#     usps_request = f"""
#     <AddressValidateRequest USERID="{USPS_USER_ID}">
#         <Address>
#             <Address1>{address.address}</Address1>
#         </Address>
#     </AddressValidateRequest>
#     """
    
#     # Set up parameters for the request
#     params = {
#         'API': 'Verify',
#         'XML': usps_request
#     }
    
#     # Send the request to USPS API
#     response = requests.get(usps_api_url, params=params)
    
#     # Check the status code of the response
#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code, detail="Error contacting USPS API")
    
#     # Process the XML response
#     try:
#         response_text = response.text
#         # You might want to add XML parsing here
#         # For example, you could use xml.etree.ElementTree or another XML library to parse and extract data
        
#         return {"usps_response": response_text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing USPS response: {e}")
