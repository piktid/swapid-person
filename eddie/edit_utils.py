import os
import sys
import json
import requests
from io import BytesIO
from PIL import Image, ImageFile, ImageFilter
from random import randint

from .edit_api import upload_target_call, upload_reference_call, generate_variation_call, open_image_from_url, handle_notifications


def process_image(PARAM_DICTIONARY, TOKEN_DICTIONARY):

    TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')

    REF_NAME = PARAM_DICTIONARY.get('REF_NAME')
    REF_PATH = PARAM_DICTIONARY.get('REF_PATH')
    REF_URL = PARAM_DICTIONARY.get('REF_URL')
    
    if REF_NAME is None and (REF_PATH is not None or REF_URL is not None):
        print('Uploading the reference image')
        response_json = upload_reference_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
        REF_NAME = response_json.get('reference_name')
        print(f'ref_name: {REF_NAME}')
        if REF_NAME is None:
            # server errors
            print('Server error, try again later')
            return False, ''

    else:
        print(f'Reference is already available with code:{REF_NAME}, proceeding..')

    PARAM_DICTIONARY['REF_NAME'] = REF_NAME

    # currently, it works only with one face in both source and target images
    if TARGET_NAME is None:
        print('Uploading the target image')
        response_json = upload_target_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
        TARGET_NAME = response_json.get('id_image')
        PARAM_DICTIONARY['TARGET_NAME'] = TARGET_NAME
    else:
        print(f'Input image is already available with code: {TARGET_NAME}, proceeding..')

    idx_person = PARAM_DICTIONARY.get('ID_PERSON', 0)
    print(f'Generating a new person using {TARGET_NAME} for idx_person: {idx_person}')
    PARAM_DICTIONARY['ID_PERSON'] = idx_person
    response_json = generate_variation_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
    print(response_json)
    
    # Asynchronous API call to get the output
    flag_response, response_notifications = handle_notifications(TARGET_NAME, idx_person, TOKEN_DICTIONARY)
    if flag_response is False:
        # Error
        print('Error retrieving the generated images. No images found after 60 attempts')
        return False, ''

    download_link = ((response_notifications.get("links"))[0]).get("l") 
    print('new edited image is ready for download:', download_link)

    return True, download_link