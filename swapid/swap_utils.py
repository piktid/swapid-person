import os
import sys
import json
import requests
from io import BytesIO
from PIL import Image, ImageFile, ImageFilter

from .consistent_identities_api import upload_target_call, upload_face_call, consistent_generation_call, handle_notifications_new_swap_download


def process_image(PARAM_DICTIONARY, TOKEN_DICTIONARY):


    FACE_NAME = PARAM_DICTIONARY.get('FACE_NAME') # it is different from REF_NAME
    TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')

    # currently, it works only with one face in both source and target images
    if FACE_NAME is None:
        print('Uploading the reference face image')
        response_json = upload_face_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
        FACE_NAME = response_json.get('identity_name')
        print(f'Face name: {FACE_NAME}')
        PARAM_DICTIONARY['FACE_NAME'] = FACE_NAME
    else:
        print(f'Input reference face is already available with code: {FACE_NAME}, proceeding..')

    if TARGET_NAME is None:
        print('Uploading the target image')
        image_id, indices_info, selected_faces_list = upload_target_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
        print(f'Target name: {image_id}')
        PARAM_DICTIONARY['TARGET_NAME'] = image_id

    else:
        print(f'Target image is already available with code: {TARGET_NAME}, proceeding..')
        image_id = PARAM_DICTIONARY['TARGET_NAME']

    idx_face = PARAM_DICTIONARY.get('ID_FACE', 0)  # select which person in the target image you want to swap with the input face
    print(f'Generating a new face using {FACE_NAME} for idx_face: {idx_face}')
    response = consistent_generation_call(idx_face=idx_face, PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
    print(response)

    # Asynchronous API call to get the output
    flag_response, response_notifications = handle_notifications_new_swap_download(image_id, idx_face, TOKEN_DICTIONARY)

    if flag_response is False:
        # Error
        print('Error retrieving the generated faces. No images found after 60 attempts')
        return False, ''

    download_link = response_notifications.get('link_hd')  # pay attention as this works only for paying customers
    print('new swapped image is ready for download:', download_link)

    return True, download_link
