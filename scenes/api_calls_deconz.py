import json

import requests

from groups.api_calls_deconz import DECONZ_GROUPS_URL

DECONZ_SCENES_URL = DECONZ_GROUPS_URL + "/" + "<GROUP_ID>" + "/scenes"


def create_scene(group_id, request_data):
    if isinstance(request_data, dict) and request_data != {}:
        response = requests.post(DECONZ_SCENES_URL.replace("<GROUP_ID>", group_id), data=json.dumps(request_data))
        response = response.json()
    else:
        response = None

    return response


def get_all_scenes(group_id):
    response = requests.get(DECONZ_SCENES_URL.replace("<GROUP_ID>", group_id))
    response = response.json()

    return response


def get_scene_attributes(group_id, scene_id):
    response = requests.get(DECONZ_SCENES_URL.replace("<GROUP_ID>", group_id) + "/" + scene_id)
    response = response.json()

    return response


def update_scene_light_state(group_id, scene_id, light_id, request_data):
    if isinstance(request_data, dict) and request_data != {}:
        response = requests.put(
            DECONZ_SCENES_URL.replace("<GROUP_ID>", group_id) + "/" + scene_id + "/lights/" + light_id,
            data=json.dumps(request_data))
        response = response.json()
    else:
        response = None

    return response


def update_scene_attributes(group_id, scene_id, request_data):
    if isinstance(request_data, dict) and request_data != {}:
        response = requests.put(DECONZ_SCENES_URL.replace("<GROUP_ID>", group_id) + "/" + scene_id,
                                data=json.dumps(request_data))
        print("LLLLLLLLLLLLLLLLLLLL",response.content)
        response = response.json()
    else:
        response = None

    return response


def store_scene(group_id, scene_id):
    response = requests.put(DECONZ_SCENES_URL.replace("<GROUP_ID>", group_id) + "/" + scene_id + "/store")
    response = response.json()

    return response


def recall_scene(group_id, scene_id):
    response = requests.put(DECONZ_SCENES_URL.replace("<GROUP_ID>", group_id) + "/" + scene_id + "/recall")
    response = response.json()

    return response


def delete_scene(group_id, scene_id):
    response = requests.delete(DECONZ_SCENES_URL.replace("<GROUP_ID>", group_id) + "/" + scene_id)
    response = response.json()

    return response
