import requests
import json
from io import BytesIO
import base64
from PIL import Image, ImageCms
from time import sleep
import os
from config import Config
from auth import refresh_call

# -----------READ/WRITE FUNCTIONS------------
def open_image_from_url(url):
    response = requests.get(url, stream=True)
    if not response.ok:
        print(response)

    image = Image.open(BytesIO(response.content))
    return image


def open_image_from_path(path):
    f = open(path, 'rb')
    buffer = BytesIO(f.read())
    image = Image.open(buffer)
    return image

def im_2_B(image):
    # Convert Image to buffer
    buff = BytesIO()

    if image.mode == 'CMYK':
        image = ImageCms.profileToProfile(image, 'ISOcoated_v2_eci.icc', 'sRGB Color Space Profile.icm', renderingIntent=0, outputMode='RGB')

    image.save(buff, format='PNG',icc_profile=image.info.get('icc_profile'))
    img_str = buff.getvalue()
    return img_str


def im_2_buffer(image):
    # Convert Image to bytes 
    buff = BytesIO()

    if image.mode == 'CMYK':
        image = ImageCms.profileToProfile(image, 'ISOcoated_v2_eci.icc', 'sRGB Color Space Profile.icm', renderingIntent=0, outputMode='RGB')

    image.save(buff, format='PNG',icc_profile=image.info.get('icc_profile'))
    return buff


def b64_2_img(data):
    # Convert Base64 to Image
    buff = BytesIO(base64.b64decode(data))
    return Image.open(buff)
    

def im_2_b64(image):
    # Convert Image 
    buff = BytesIO()
    image.save(buff, format='PNG')
    img_str = base64.b64encode(buff.getvalue()).decode('utf-8')
    return img_str


# -----------PROCESSING FUNCTIONS------------

# UPLOAD ENDPOINTS
def upload_target_call(PARAM_DICTIONARY):

    OPTIONS_DICT = PARAM_DICTIONARY.get('OPTIONS', {})

    # start the generation process given the image parameters
    target_full_path = PARAM_DICTIONARY.get('TARGET_PATH')
    if target_full_path is None:
        target_url = PARAM_DICTIONARY.get('TARGET_URL')
        # request with url
        response = requests.post(Config.URL_API+'/edit/target', 
                                 headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                                 data={'url': target_url, 'options': json.dumps(OPTIONS_DICT)},
                                 )

        if response.status_code == 401:
            refresh_call()
            # try with new TOKEN
            response = requests.post(Config.URL_API+'/edit/target', 
                                     headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                                     data={'url': target_url, 'options': json.dumps(OPTIONS_DICT)},
                                     )
    else:
        image_file = open(target_full_path, 'rb')
        # request with file
        response = requests.post(Config.URL_API+'/edit/target', 
                                 headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                                 files={'file': image_file},
                                 data={'options': json.dumps(OPTIONS_DICT)},
                                 )

        if response.status_code == 401:
            refresh_call()
            # try with new TOKEN
            response = requests.post(Config.URL_API+'/edit/target', 
                                     headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                                     files={'file': image_file},
                                     data={'options': json.dumps(OPTIONS_DICT)},
                                     )

    response_json = json.loads(response.text)
    print(f"Upload successful. Response json: {response_json}")

    return response_json


def upload_reference_call(PARAM_DICTIONARY):

    reference_full_path = PARAM_DICTIONARY.get('REF_PATH')
    if reference_full_path is None:
        reference_url = PARAM_DICTIONARY.get('REF_URL')
        image_response = requests.get(reference_url)
        image_response.raise_for_status()  
        image_file = BytesIO(image_response.content)
        image_file.name = 'reference.jpg' 
    else:
        image_file = open(reference_full_path, 'rb')

    # start the generation process given the image parameters
    response = requests.post(Config.URL_API+'/edit/reference', 
                             headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                             files={'reference': image_file},
                             )

    if response.status_code == 401:
        refresh_call()
        # try with new TOKEN
        response = requests.post(Config.URL_API+'/edit/reference', 
                                 headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                                 files={'reference': image_file},
                                 )

    response_json = json.loads(response.text)
    print(f"Upload successful. Response json: {response_json}")

    return response_json


def generate_variation_call(PARAM_DICTIONARY):

    CATEGORY = PARAM_DICTIONARY.get('CATEGORY', 'person')
    TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')
    PROMPT = PARAM_DICTIONARY.get('PROMPT')
    ID_PERSON = PARAM_DICTIONARY.get('ID_PERSON')

    data = {
            'category': CATEGORY,
            'id_image': TARGET_NAME,
            'id_person': ID_PERSON
        }

    if PROMPT is not None:
        data = {**data, 'prompt': PROMPT}


    GUIDANCE_SCALE = PARAM_DICTIONARY.get('GUIDANCE_SCALE')
    PROMPT_STRENGTH = PARAM_DICTIONARY.get('PERSON_STRENGTH')
    CONTROLNET_SCALE = PARAM_DICTIONARY.get('CONTROLNET_SCALE')
    VAR_STRENGTH = PARAM_DICTIONARY.get('VAR_STRENGTH')

    SEED = PARAM_DICTIONARY.get('SEED')

    REF_NAME = PARAM_DICTIONARY.get('REF_NAME')
    OPTIONS_DICT = PARAM_DICTIONARY.get('OPTIONS', {})

    if PROMPT_STRENGTH is not None:
        OPTIONS_DICT = {**OPTIONS_DICT, 'strength': PROMPT_STRENGTH}

    if VAR_STRENGTH is not None:
        OPTIONS_DICT = {**OPTIONS_DICT, 'var_strength': VAR_STRENGTH}

    if GUIDANCE_SCALE is not None:
        OPTIONS_DICT = {**OPTIONS_DICT, 'guidance_scale': GUIDANCE_SCALE}

    if CONTROLNET_SCALE is not None:
        OPTIONS_DICT = {**OPTIONS_DICT, 'controlnet_scale': CONTROLNET_SCALE}

    if SEED is not None:
        OPTIONS_DICT = {**OPTIONS_DICT, 'seed': SEED}

    if REF_NAME is not None:
        # force reference guidelines to 1
        OPTIONS_DICT = {**OPTIONS_DICT, 'ip_scale': 1, 'reference_name': REF_NAME}

    data = {**data, 'options': json.dumps(OPTIONS_DICT)}

    print(f'data to send to generation: {data}')

    # start the generation process given the image parameters
    response = requests.post(Config.URL_API+'/edit/generate',
                             headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                             json=data
                             )
    # if the access token is expired
    if response.status_code == 401:
        refresh_call()
        # try with new TOKEN
        response = requests.post(Config.URL_API+'/edit/generate',
                                 headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                                 json=data
                                 )

    # print(response.text)
    response_json = json.loads(response.text)
    return response_json


# -----------NOTIFICATIONS FUNCTIONS------------
def get_notification_by_name(name_list):
    # name_list='new_generation, progress, error'
    response = requests.post(Config.URL_API+'/notification_by_name_json',
                             headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                             json={'name_list': name_list},
                             )
    # if the access token is expired
    if response.status_code == 401:
        # try with new TOKEN
        refresh_call()
        response = requests.post(Config.URL_API+'/notification_by_name_json',
                                 headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                                 json={'name_list': name_list},
                                 )
    # print(response.text)
    response_json = json.loads(response.text)
    return response_json.get('notifications_list')


def delete_notification(notification_id):
    print(f'notification_id: {notification_id}')
    response = requests.delete(Config.URL_API+'/notification/delete_json',
                            headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                            json={'id': notification_id},
                            )
    # if the access token is expired
    if response.status_code == 401:
        # try with new TOKEN
        refresh_call()
        response = requests.delete(Config.URL_API+'/notification/delete_json',
            headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
            json={'id':notification_id},
        )

    # print(response.text)
    return response.text


def handle_notifications(image_id, idx_person):

    # check notifications to verify the generation status
    i = 0
    while i < 120:  # max 120 iterations -> then timeout
        i = i+1
        notifications_list = get_notification_by_name('edit_generate')
        #print(notifications_list)
        notifications_to_remove = [n for n in notifications_list if (n.get('name') == 'edit_generate' and n.get('data').get('address') == image_id and n.get('data').get('id_person') == idx_person)]

        #print(f'notifications_to_remove: {notifications_to_remove}')
        # remove notifications
        result_delete = [delete_notification(n.get('id')) for n in notifications_to_remove]
        #print(result_delete)

        if len(notifications_to_remove) > 0:
            print(f'download for image_id {image_id} completed')
            return True, {**notifications_to_remove[0].get('data', {})}

        # wait
        print('waiting for notification...')
        sleep(5)

    return False, {}
