import scenes.api_calls_deconz as deconz_api
from devices.helper import format_light_attributes_for_deconz
from devices.helper import get_device_data_from_deconz
from groups.models import Group
from main.views import TEST


def format_scene_data_from_deconz(scene_id, data):
    response = {"id": scene_id,
                "name": data["name"] if "name" in data.keys() else "unknown scene name",
                "lights": []
                }

    if "lights" in data.keys() and data["lights"] != []:
        for entry in data["lights"]:
            if "id" in entry.keys():
                response["lights"] += [{"id": entry["id"],
                                        "name": get_device_data_from_deconz(entry["id"])["name"],
                                        "on": entry["on"] if "on" in entry.keys() else False,
                                        "brightness": int(
                                            entry["bri"] / 255 * 100) if "bri" in
                                                                         entry.keys() else 0,
                                        "hue": int(
                                            entry["hue"] / 65535 * 360) if "hue" in
                                                                           entry.keys() else 0,
                                        "saturation": int(
                                            entry["sat"] / 255 * 100) if "sat" in
                                                                         entry.keys() else 0
                                        }]

    return response


def get_scene_data_from_deconz(group_id, scene_id=None, username=None):
    if not (isinstance(group_id, int) or isinstance(group_id, str) and group_id.isnumeric()):
        return {"error": "group id is not valid"}

    if scene_id is None:
        response = []

        if not TEST:
            response_scenes = deconz_api.get_all_scenes(group_id)

            for key, value in response_scenes.items():
                response_scene_tmp = deconz_api.get_scene_attributes(group_id, key)
                response_scene_tmp = response_scene_tmp.json()

                response += [format_scene_data_from_deconz(key, response_scene_tmp)]
        else:
            if group_id == "1":
                response_scenes = {
                    "1": {
                        "lights": ["1", "2"],
                        "name": "working"
                    },
                    "2": {
                        "lights": ["4", "6", "7", "5"],
                        "name": "reading"
                    }
                }
            elif group_id == "2":
                response_scenes = {
                    "3": {
                        "lights": ["2", "4", "7"],
                        "name": "holiday"
                    },
                    "4": {
                        "lights": ["3"],
                        "name": "BIERPAUSE"
                    },
                    "8": {
                        "lights": ["3", "2"],
                        "name": "sleeping"
                    }
                }
            else:
                response_scenes = {
                    "5": {
                        "lights": ["4", "6", "7", "5"],
                        "name": "work out"
                    },
                    "6": {
                        "lights": ["3"],
                        "name": "Party"
                    }
                }

            print("huren scenes", response_scenes)
            for key, value in response_scenes.items():
                print("key", key, "value", value, "du ficker")
                key = key.__str__()
                if key == "1":
                    print("unos")
                    response_scene_tmp = {
                        "lights": [
                            {
                                "bri": 111,
                                "hue": 32425,
                                "sat": 123,
                                "id": "3",
                                "on": False,
                                "transitiontime": 0,
                                "x": 27499,
                                "y": 26060
                            },
                            {
                                "bri": 200,
                                "hue": 43525,
                                "sat": 234,
                                "id": "4",
                                "on": True,
                                "transitiontime": 0,
                                "x": 27499,
                                "y": 26060
                            },
                            {
                                "bri": 98,
                                "hue": 12425,
                                "sat": 43,
                                "id": "5",
                                "on": True,
                                "transitiontime": 0,
                                "x": 27499,
                                "y": 26060
                            }
                        ],
                        "name": "reading",
                        "state": 0
                    }
                elif key == "2":
                    print("duoes")
                    response_scene_tmp = {
                        "lights": [
                            {
                                "bri": 200,
                                "hue": 12344,
                                "sat": 23,
                                "id": "4",
                                "on": True,
                                "transitiontime": 0,
                                "x": 27499,
                                "y": 26060
                            },
                            {
                                "bri": 98,
                                "hue": 55555,
                                "sat": 233,
                                "id": "5",
                                "on": True,
                                "transitiontime": 0,
                                "x": 27499,
                                "y": 26060
                            }
                        ],
                        "name": "Netflix",
                        "state": 0
                    }
                else:
                    print("tries", key)
                    response_scene_tmp = {
                        "lights": [
                            {
                                "bri": 98,
                                "id": "5",
                                "on": True,
                                "transitiontime": 0,
                                "x": 27499,
                                "y": 26060
                            }
                        ],
                        "name": "workout",
                        "state": 0
                    }

                response += [format_scene_data_from_deconz(key, response_scene_tmp)]

        return response
    elif isinstance(scene_id, int) or isinstance(scene_id, str) and scene_id.isnumeric():
        response = deconz_api.get_scene_attributes(group_id, scene_id)
        response = format_scene_data_from_deconz(scene_id, response)

        return response
    else:
        return {"error": "scene id is not valid"}


def get_all_scene_data_from_deconz(username):
    if TEST:
        # response_groups = get_all_groups()
        #
        # response = {}
        # for key in response_groups.keys():
        #     response[key] = get_scene_data_from_deconz(key, username)

        scenes_group = Group.objects.get(name="___scenes_group_deconz___").__dict__
        scenes_group_id = scenes_group["group_id"]

        response = get_scene_data_from_deconz(scenes_group_id, username=username)
    else:
        response = {}

    return response


def update_scene_deconz(scene_id, request_data):
    if not (isinstance(scene_id, int) or isinstance(scene_id, str) and scene_id.isnumeric()):
        return {"error", "scene id is not valid"}

    if isinstance(request_data, dict) and request_data != {}:
        for key, value in request_data.items():
            if not (isinstance(key, int) or isinstance(key, str) and key.isnumeric()):
                return {"error": "request data keys contains a non id"}
            if not isinstance(value, dict):
                return {"error": "values of request data in wrong format"}
            if not set(value.keys()) <= set(update_scene_light_state_deconz.__code__.co_varnames):
                return {"error": "values of request data contain unknown keys"}

        for key, value in request_data.items():
            update_scene_light_state_deconz(scene_id, key, **value)
    else:
        return {"error": "no request data or wrong format"}


def update_scene_light_state_deconz(scene_id, light_id, alert=None, brightness=None, color_loop_speed=None, ct=None,
                                    effect=None,
                                    hue=None, on=None,
                                    saturation=None, transition_time=None, x=None, y=None):
    zwErg = format_light_attributes_for_deconz(alert, brightness, color_loop_speed, ct, effect, hue, on, saturation,
                                               transition_time, x, y)
    response = deconz_api.update_scene_light_state(scene_id.__str__(), light_id.__str__(), zwErg["request_data"])

    return {"error": zwErg["error"], "response": response}
