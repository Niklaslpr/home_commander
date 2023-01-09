import json
import requests
from groups.api_calls_deconz import DECONZ_GROUPS_URL

DECONZ_SCENES_URL = DECONZ_GROUPS_URL + "/" + "<GROUP_ID>" + "/scenes"


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
        response = requests.put(DECONZ_SCENES_URL.replace("<GROUP_ID>", group_id) + "/" + scene_id + "/lights/" + light_id)
    else:
        response = None

    return response
