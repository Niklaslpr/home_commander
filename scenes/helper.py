import scenes.api_calls_deconz as deconz_api
from main.views import TEST
from devices.helper import format_light_attributes_for_deconz
from groups.api_calls_deconz import get_all_groups


def format_scene_data_from_deconz(scene_id, data):
    return None
    # return {"id": device_id,
    #         "has_color": data["hascolor"] if "hascolor" in data.keys() else False,
    #         "name": data["name"] if "name" in data.keys() else "unknown device name",
    #         "type": data["type"] if "type" in data.keys() else "unknown device type",
    #         "reachable": data["state"]["reachable"] if "state" in data.keys() and "reachable" in
    #                                                    data[
    #                                                        "state"].keys() else False,
    #         "on": data["state"]["on"] if "state" in data.keys() and "on" in data[
    #             "state"].keys() else False,
    #         "brightness": int(data["state"]["bri"] / 255 * 100) if "state" in data.keys() and "bri" in
    #                                                                data["state"].keys() else 0,
    #         "hue": int(data["state"]["hue"] / 65535 * 360) if "state" in data.keys() and "hue" in
    #                                                           data[
    #                                                               "state"].keys() else 0,
    #         "saturation": int(data["state"]["sat"] / 255 * 100) if "state" in data.keys() and "sat" in
    #                                                                data["state"].keys() else 0
    #         }


def get_scene_data_from_deconz(group_id, username, scene_id=None):
    if not (isinstance(group_id, int) or isinstance(group_id, str) and group_id.isnumeric()):
        return {"error": "group id is not valid"}

    if scene_id is None:
        response = {}

        if not TEST:
            response_scenes = deconz_api.get_all_scenes(group_id)

            response_tmp = []
            for key, group in response_scenes.items():
                response_scene_tmp = deconz_api.get_scene_attributes(group_id, key)
                response_scene_tmp = response_scene_tmp.json()

                response_tmp += [format_scene_data_from_deconz(key, response_scene_tmp)]

            response[group_id] = response_tmp
        else:
            response_groups = {
                "1": {
                    "devicemembership": [],
                    "etag": "ab5272cfe11339202929259af22252ae",
                    "hidden": False,
                    "name": "Living Room"
                },
                "2": {
                    "devicemembership": ["3"],
                    "etag": "030cf8c1c0025420f3a0659afab251f5",
                    "hidden": False,
                    "name": "Kitchen"
                }
            }

            response_tmp = {}
            for key, group in response_groups.items():
                if key == "1":
                    response_scenes_tmp = {
                        "1": {
                            "lights": ["1", "2"],
                            "name": "working"
                        },
                        "2": {
                            "lights": ["4", "6", "7", "5"],
                            "name": "reading"
                        }
                    }
                elif key == "2":
                    response_scenes_tmp = {
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
                    response_scenes_tmp = {
                        "5": {
                            "lights": ["4", "6", "7", "5"],
                            "name": "work out"
                        },
                        "6": {
                            "lights": ["3"],
                            "name": "Party"
                        }
                    }

        return response
    elif isinstance(scene_id, int) or isinstance(scene_id, str) and scene_id.isnumeric():
        response = deconz_api.get_scene_attributes(group_id, scene_id)
        response = format_scene_data_from_deconz(scene_id, response)

        return response
    else:
        return {"error": "scene id is not valid"}


def get_all_scene_data_from_deconz(username):
    if not TEST:
        response_groups = get_all_groups()

        response = {}
        for key in response_groups.keys():
            response[key] = get_scene_data_from_deconz(key, username)
    else:
        pass

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


def update_scene_light_state_deconz(scene_id, light_id, alert=None, brightness=None, color_loop_speed=None, ct=None, effect=None,
                              hue=None, on=None,
                              saturation=None, transition_time=None, x=None, y=None):
    zwErg = format_light_attributes_for_deconz(alert, brightness, color_loop_speed, ct, effect, hue, on, saturation, transition_time, x, y)
    response = deconz_api.update_scene_light_state(scene_id.__str__(), light_id.__str__(), zwErg["request_data"])

    return {"error": zwErg["error"], "response": response}
