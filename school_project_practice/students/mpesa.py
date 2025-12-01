import requests
import json
import base64
from datetime import datetime

# 1. YOUR CREDENTIALS
CONSUMER_KEY = 'K5mHxd2ml7a8Gz5UK4cpx5XsudKrqSGqXner4s5PxnnvGEtu'
CONSUMER_SECRET = 'WlpLTZgGGUTBi7nTPoy1EzD3jD3Spf7Yc6PJJgXP79A8KtBQ4uy6HtzP6dhZeWSA'
BUSINESS_SHORTCODE = '174379'
PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

# This points to your LIVE PythonAnywhere site
CALLBACK_URL = 'https://kinariportal.pythonanywhere.com/api/payment-callback/' 

def get_access_token():
    """Authenticates with Safaricom and gets a temporary token."""
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    r = requests.get(api_URL, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    
    # Check if we got a valid token
    if r.status_code == 200:
        return r.json()['access_token']
    else:
        raise Exception(f"Failed to get Access Token: {r.text}")

def lipa_na_mpesa(phone_number, amount, account_ref="KinariFees"):
    """Triggers the STK Push to the parent's phone."""
    try:
        access_token = get_access_token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        
        # Generate the Password required by Safaricom
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_str = BUSINESS_SHORTCODE + PASSKEY + timestamp
        password = base64.b64encode(password_str.encode()).decode('utf-8')
        
        # Format phone number (Must be 254...)
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
            
        payload = {
            "BusinessShortCode": BUSINESS_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number, # The phone sending money
            "PartyB": BUSINESS_SHORTCODE, # The Paybill receiving money
            "PhoneNumber": phone_number,
            "CallBackURL": CALLBACK_URL,
            "AccountReference": account_ref,
            "TransactionDesc": "School Fees Payment"
        }
        
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
        
        response = requests.post(api_url, json=payload, headers=headers)
        return response.json()
        
    except Exception as e:
        return {'ResponseCode': '1', 'errorMessage': str(e)}