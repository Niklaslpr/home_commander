from main.views import TEST

import rooms.api_calls_deconz as deconz_api
from devices.helper import get_device_data_from_deconz # TODO: check if sensors and lights have their own id counter


def get_group_data_from_deconz(id, username):
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
            if key == "20000":
                pass
            else:

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
                            "name": "__group_all_LivingroomGroupTest2",
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
                print("WARUM MAN ", zwErg)
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

                # if (zwErg["name"].split("_")[2] if "name" in zwErg.keys() else "") == "group" and (
                        # zwErg["name"].split("_")[3] if "name" in zwErg.keys() else "") in ["all", username]:
                
                
                # Pass the favorite-groups
                if zwErg["name"].split("_")[0] == "favorites":
                    pass
                else:
                
                    response += [{"id": key,
                                  "name": zwErg["name"] if "name" in zwErg.keys() else "unknown group name",
                                  "devices": devices,
                                  "on": zwErg["action"]["on"] if "action" in zwErg.keys() and "on" in zwErg[
                                      "action"].keys() else False,
                                  "brightness": int(
                                      zwErg["action"]["bri"] / 255 * 100) if "action" in zwErg.keys() and "bri" in zwErg[
                                      "action"].keys() else 0,
                                  "hue": int(zwErg["action"]["hue"] / 65535 * 360) if "action" in zwErg.keys() and "hue" in
                                                                                      zwErg["action"].keys() else 0,
                                  "saturation": int(
                                      zwErg["action"]["sat"] / 255 * 100) if "action" in zwErg.keys() and "sat" in zwErg[
                                      "action"].keys() else 0
                                  }]
                    
                # else:
                    # # nothing so far
                    # pass
        
        return response
    else:
        response = deconz_api.get_group_attributes(id)
        response = response.json()

        return response
