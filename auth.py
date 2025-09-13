import requests
import json
import os
from config import Config

# -----------AUTH FUNCTIONS------------

def start_call(email, password):
    print(f'Logging to: {Config.URL_API}')

    response = requests.post(Config.URL_API+'/tokens', data={}, auth=(email, password))
    response_json = json.loads(response.text)
    ACCESS_TOKEN = response_json['access_token']
    REFRESH_TOKEN = response_json['refresh_token']
    if ACCESS_TOKEN is None or REFRESH_TOKEN is None:
        print('Error logging in, please check your credentials.')
        return {}

    return {'access_token': ACCESS_TOKEN, 'refresh_token': REFRESH_TOKEN}


def piktid_auth():
    # Check if the token is stored in the env variables
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', None)
    REFRESH_TOKEN = os.getenv('REFRESH_TOKEN', None)
    
    if ACCESS_TOKEN is None or REFRESH_TOKEN is None:
        print('ACCESS_TOKEN or REFRESH_TOKEN environment variables not found. Please set them to proceed.')
        
        # Check if the email and password are stored in the env variables
        PIKTID_EMAIL = os.getenv("PIKTID_EMAIL")
        PIKTID_PASSWORD = os.getenv("PIKTID_PASSWORD")

        if PIKTID_EMAIL is None or PIKTID_PASSWORD is None:
            print('EMAIL or PASSWORD environment variables not found. Please set them to proceed.')
            return False

        TOKEN_DICTIONARY = start_call(email=PIKTID_EMAIL, password=PIKTID_PASSWORD, server_mode='production')
        # Save the tokens in the environment variables for future use
        os.environ['ACCESS_TOKEN'] = TOKEN_DICTIONARY.get('access_token', '')
        os.environ['REFRESH_TOKEN'] = TOKEN_DICTIONARY.get('refresh_token', '')

        return True
    
    return True

def refresh_call():
    # Get token using only access and refresh tokens, no mail and psw
    
    # Check if the token is stored in the env variables
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', None)
    REFRESH_TOKEN = os.getenv('REFRESH_TOKEN', None)
    if ACCESS_TOKEN is None or REFRESH_TOKEN is None:
        print('ACCESS_TOKEN or REFRESH_TOKEN environment variables not found. Please set them to proceed.')
        return False
    
    TOKEN_DICTIONARY = {
        'access_token': ACCESS_TOKEN,
        'refresh_token': REFRESH_TOKEN
    }

    response = requests.put(Config.URL_API+'/tokens', json=TOKEN_DICTIONARY)
    response_json = json.loads(response.text)
    ACCESS_TOKEN = response_json['access_token']
    REFRESH_TOKEN = response_json['refresh_token']
    
    if ACCESS_TOKEN is None or REFRESH_TOKEN is None:
        print('Error refreshing token, please check your credentials.')
        
        # Check if the email and password are stored in the env variables
        PIKTID_EMAIL = os.getenv("PIKTID_EMAIL")
        PIKTID_PASSWORD = os.getenv("PIKTID_PASSWORD")

        if PIKTID_EMAIL is None or PIKTID_PASSWORD is None:
            print('EMAIL or PASSWORD environment variables not found. Please set them to proceed.')
            return False
        
        TOKEN_DICTIONARY = start_call(email=PIKTID_EMAIL, password=PIKTID_PASSWORD, server_mode='production')
        # Save the tokens in the environment variables for future use
        os.environ['ACCESS_TOKEN'] = TOKEN_DICTIONARY.get('access_token', '')
        os.environ['REFRESH_TOKEN'] = TOKEN_DICTIONARY.get('refresh_token', '')

        return True

    # Save the tokens in the environment variables for future use
    os.environ['ACCESS_TOKEN'] = ACCESS_TOKEN
    os.environ['REFRESH_TOKEN'] = REFRESH_TOKEN

    return True