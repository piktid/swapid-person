import os
import sys
import json
import argparse
from io import BytesIO
from random import randint
from PIL import Image, ImageFile, ImageFilter

from swapid.swap_utils import process_image as process_swap
from eddie.edit_utils import process_image as process_person
from eddie.edit_api import start_call


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # INPUT IMAGE PARAMETERS
    parser.add_argument('--target_path', help='Input image file absolute path', type=str, default=None)
    parser.add_argument('--target_url', help='Input image url, use only if no target path was given', type=str, default='https://images.piktid.com/frontend/studio/swapid/target/monalisa.jpg')

    parser.add_argument('--reference_path', help='Input reference file absolute path', type=str, default=None)
    parser.add_argument('--reference_url', help='Input reference url, use only if no reference path was given', type=str, default='https://images.piktid.com/frontend/studio/swapid/face/einstein.jpg')

    parser.add_argument('--target_name', help='Target image code name (id image), it overwrites the target path', type=str, default=None)
    parser.add_argument('--reference_name', help='Reference image code name, it overwrites the reference path', type=str, default=None)

    # INPUT PARAMETERS
    parser.add_argument('--seed', help='Generation seed', type=int, default=randint(0, 1000000))
    parser.add_argument('--prompt', help='Target image description', type=str, default=None)
    parser.add_argument('--controlnet_scale', help='Resemblance with the target face (range 0-2)', type=float, default=None)
    parser.add_argument('--guidance_scale', help='Guidance scale (range 1-20)', type=float, default=None)
    
    # EDIT PARAMETERS
    parser.add_argument('--person_strength', help='Similarity with the reference person level (range 0-1)', type=float, default=None)
    parser.add_argument('--var_strength', help='Creativity level (range 0-1)', type=float, default=None)
    parser.add_argument('--id_person', help='Person to modify', type=int, default=0)

    # SWAP PARAMETERS
    parser.add_argument('--body', help='Change also the body', action='store_true')
    parser.add_argument('--hair', help='Change also the hair', action='store_true')
    parser.add_argument('--swap_strength', help='Similarity with the reference face level (range 0-1)', type=float, default=None)
    parser.add_argument('--id_face', help='Index of the face to change in the target image', type=int, default=0)

    args = parser.parse_args()

    # be sure to export your email and psw as environmental variables
    EMAIL = os.getenv("SWAPID_EMAIL")
    PASSWORD = os.getenv("SWAPID_PASSWORD")

    # GLOBAL PARAMETERS
    PROMPT = args.prompt
    CONTROLNET_SCALE = args.controlnet_scale
    GUIDANCE_SCALE = args.guidance_scale
    SEED = args.seed

    # EDIT PARAMETERS
    BODYSWAP = args.body  # True if the swap shall include the body (Body-swap)
    ID_PERSON = args.id_person
    PERSON_STRENGTH = args.person_strength
    VAR_STRENGTH = args.var_strength

    # SWAP PARAMETERS
    HEADSWAP = args.hair  # True if the swap shall include the hair (Head-swap)
    ID_FACE = args.id_face  # index of the person in the target image to swap
    SWAP_STRENGTH = args.swap_strength

    # INPUT IMAGE PARAMETERS
    TARGET_PATH = args.target_path
    TARGET_URL = args.target_url
    TARGET_NAME = args.target_name

    # REFERENCE IMAGE PARAMETERS
    REF_PATH = args.reference_path
    REF_URL = args.reference_url
    REF_NAME = args.reference_name

    if TARGET_PATH is not None:
        if os.path.exists(TARGET_PATH):
            print(f'Using as input image the file located at: {TARGET_PATH}')
        else:
            print('Wrong filepath, check again')
    else:
        print('Target filepath not assigned, check again')
        if TARGET_URL is not None:
            print(f'Using the input image located at: {TARGET_URL}')
        else:
            print('Wrong target url, check again')
            sys.exit()

    if REF_PATH is not None:
        if os.path.exists(REF_PATH):
            print(f'Using the input reference located at: {REF_PATH}')
        else:
            print('Wrong face path, check again')
            sys.exit()
    else:
        print('Face path not assigned, check again')
        if REF_URL is not None:
            print(f'Using the input reference located at: {REF_URL}')
        else:
            print('Wrong face url, check again')
            sys.exit()

    # log in or use token
    TOKEN_DICTIONARY = start_call(EMAIL, PASSWORD)

    print(TOKEN_DICTIONARY)

    # initialize the parameters dictionary
    PARAM_DICTIONARY = {

            'TARGET_PATH': TARGET_PATH,
            'TARGET_URL': TARGET_URL,
            'REF_PATH': REF_PATH,
            'REF_URL': REF_URL,
            'TARGET_NAME': TARGET_NAME,
            'REF_NAME': REF_NAME,

            'PROMPT': PROMPT,
            'SEED': SEED,
            'CONTROLNET_SCALE': CONTROLNET_SCALE,
            'GUIDANCE_SCALE': GUIDANCE_SCALE,

            'PERSON_STRENGTH': PERSON_STRENGTH,
            'VAR_STRENGTH': VAR_STRENGTH,
            'ID_PERSON': ID_PERSON,

            'SWAP_STRENGTH': SWAP_STRENGTH,
            'ID_FACE': ID_FACE,
            'HEADSWAP': HEADSWAP
        }

    # --------------------------------
    # PROCESSING STARTS HERE
    if BODYSWAP:
        # generate the full body based on the reference face
        response, image_edited_person_link = process_person(PARAM_DICTIONARY, TOKEN_DICTIONARY)
        
        # reset the target image parameters
        PARAM_DICTIONARY['TARGET_NAME'] = None
        PARAM_DICTIONARY['TARGET_PATH'] = None
        PARAM_DICTIONARY['TARGET_URL'] = image_edited_person_link

    # swap the reference face on the target edited image
    response, image_edited_swap_link = process_swap(PARAM_DICTIONARY, TOKEN_DICTIONARY)
