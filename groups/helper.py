import groups.api_calls_deconz as deconz_api
from devices.helper import \
    get_device_data_from_deconz  # TODO: check if sensors and lights have their own id counter -> yes!!!
from main.views import TEST


def format_group_data_from_deconz(group_id, data, devices=None):
    return {"id": group_id,
            "name": data["name"].split("_")[4] if "name" in data.keys() else "unknown group name",
            "devices": devices if devices is not None else [],
            "on": data["action"]["on"] if "action" in data.keys() and "on" in data[
                "action"].keys() else False,
            "brightness": int(
                data["action"]["bri"] / 255 * 100) if "action" in data.keys() and "bri" in data[
                "action"].keys() else 0,
            "hue": int(data["action"]["hue"] / 65535 * 360) if "action" in data.keys() and "hue" in
                                                                data["action"].keys() else 0,
            "saturation": int(
                data["action"]["sat"] / 255 * 100) if "action" in data.keys() and "sat" in data[
                "action"].keys() else 0
            }


def format_group_attributes_for_deconz(name=None, lights=None, hidden=None, light_sequence=None, multi_device_ids=None):
    request_data = {}
    errors = []

    if name is not None and isinstance(name, str) and 0 < name.__len__() <= 32:
        request_data["name"] = name
    elif name is not None:
        errors += ["name"]

    if lights is not None and isinstance(lights, list):
        request_data["lights"] = lights
    elif lights is not None:
        errors += ["lights"]

    if hidden is not None and (
            isinstance(hidden, bool) or isinstance(hidden, str) and hidden in ["True", "true", "False", "false"]):
        if isinstance(hidden, str) and hidden in ["False", "false"]:
            request_data["hidden"] = bool(0)
        else:
            request_data["hidden"] = bool(hidden)
    elif hidden is not None:
        errors += ["hidden"]

    if light_sequence is not None and isinstance(light_sequence, list):
        request_data["lightsequence"] = light_sequence
    elif light_sequence is not None:
        errors += ["lightsequence"]

    if multi_device_ids is not None and isinstance(multi_device_ids, list):
        request_data["mulitdeviceids"] = multi_device_ids
    elif multi_device_ids is not None:
        errors += ["mulitdeviceids"]

    return {"error": errors, "request_data": request_data}


def create_group_in_deconz(name, username=None):
    response = deconz_api.create_group({"name": name})
    print("create response:", response)

    return response


def get_group_data_from_deconz(id, username=None):
    if id == -1:
        if not TEST:
            response_tmp = deconz_api.get_all_groups()
        else:
            response_tmp = {
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

        response = []
        for key, value in response_tmp.items():

            if not TEST:
                zwErg = deconz_api.get_group_attributes(key)
            else:
                if key == "1":
                    zwErg = {
                        "action": {
                            "bri": 0,
                            "ct": 500,
                            "effect": "none",
                            "hue": 0,
                            "on": False,
                            "sat": 0,
                            "xy": [0, 0]
                        },
                        "devicemembership": [],
                        "etag": "0b32030b31ef30a4446c9adff6a6f9e5",
                        "hidden": False,
                        "id": "32772",
                        "lights": ["3", "42", "43"],
                        "lightsequence": ["42", "43", "3"],
                        "multideviceids": ["2"],
                        "name": "__group_all_LivvingroomGroupTest2",
                        "scenes": [
                            {"id": "1", "name": "warmlight"}
                        ],
                        "state": 0
                    }
                else:
                    zwErg = {
                        "action": {
                            "bri": 25,
                            "ct": 100,
                            "effect": "colorloop",
                            "hue": 235,
                            "on": False,
                            "sat": 12,
                            "xy": [0, 0]
                        },
                        "devicemembership": [],
                        "etag": "0b32030b31ef30a4446c9adff6a6f9e5",
                        "hidden": False,
                        "id": "32773",
                        "lights": ["1", "2", "3"],
                        "lightsequence": ["2", "1"],
                        "multideviceids": [],
                        "name": "__group_all_BedroomGroupTest1",
                        "scenes": [
                            {"id": "2", "name": "coldlight"}
                        ],
                        "state": 0
                    }

            print("EY JO 2", zwErg["name"].split("_")[0])
            print("xxx", username)

            devices = []
            if not TEST:
                if "lights" in zwErg.keys():
                    for entry in zwErg["lights"]:
                        # TODO: request.get(DECONZ_DEVICE_LIGHTS_URL + "/" + entry)
                        nameZwErg = get_device_data_from_deconz(entry, username)
                        nameZwErg = nameZwErg["name"] if "name" in nameZwErg.keys() else "unknown name"
                        devices += [{"type": "light", "id": entry, "name": nameZwErg}]
            else:
                if "lights" in zwErg.keys():
                    for entry in zwErg["lights"]:
                        nameZwErg = {"name": "Licht " + entry}
                        nameZwErg = nameZwErg["name"] if "name" in nameZwErg.keys() else "unknown name"
                        devices += [{"type": "light", "id": entry, "name": nameZwErg}]

            # devices = [["light", request.get().json(), entry] for entry in zwErg["lights"]] if "lights" in zwErg.keys() else []

            # TODO: Loop over Sensors to find all Sensors related to that Group!

            if (zwErg["name"].split("_")[2] if "name" in zwErg.keys() else "") == "group" and (
                    zwErg["name"].split("_")[3] if "name" in zwErg.keys() else "") in ["all", username]:
                response += [format_group_data_from_deconz(key, zwErg, devices)]
            else:
                # nothing so far
                pass

        return response
    else:
        response = deconz_api.get_group_attributes(id)
        response = response.json()

        return response


def update_group_deconz(group_id, name=None, lights=None, hidden=None, light_sequence=None, multi_device_ids=None):
    zwErg = format_group_attributes_for_deconz(name, lights, hidden, light_sequence, multi_device_ids)

    response = deconz_api.update_group_attributes(group_id.__str__(), zwErg["request_data"])

    return {"error": zwErg["error"], "response": response}
