import devices.api_calls_deconz as deconz_api
from main.views import TEST


def format_device_data_from_deconz(device_id, data):
    return {"id": device_id,
            "has_color": data["hascolor"] if "hascolor" in data.keys() else False,
            "name": data["name"] if "name" in data.keys() else "unknown device name",
            "type": data["type"] if "type" in data.keys() else "unknown device type",
            "reachable": data["state"]["reachable"] if "state" in data.keys() and "reachable" in
                                                       data[
                                                           "state"].keys() else False,
            "on": data["state"]["on"] if "state" in data.keys() and "on" in data[
                "state"].keys() else False,
            "brightness": int(data["state"]["bri"] / 255 * 100) if "state" in data.keys() and "bri" in
                                                                   data["state"].keys() else 0,
            "hue": int(data["state"]["hue"] / 65535 * 360) if "state" in data.keys() and "hue" in
                                                              data[
                                                                  "state"].keys() else 0,
            "saturation": int(data["state"]["sat"] / 255 * 100) if "state" in data.keys() and "sat" in
                                                                   data["state"].keys() else 0
            }


def format_light_attributes_for_deconz(alert=None, brightness=None, color_loop_speed=None, ct=None, effect=None,
                                       hue=None, on=None,
                                       saturation=None, transition_time=None, x=None, y=None):
    request_data = {}
    errors = []

    if alert is not None and alert in ["none", "select", "lselect"]:
        request_data["alert"] = alert
    elif alert is not None:
        errors += ["alert"]

    if brightness is not None and (isinstance(brightness, int) or isinstance(brightness,
                                                                             str) and brightness.isnumeric()) and 0 <= brightness <= 255:
        request_data["bri"] = int(brightness)
    elif brightness is not None:
        errors += ["brightness"]

    if color_loop_speed is not None and (isinstance(color_loop_speed, int) or isinstance(color_loop_speed,
                                                                                         str) and color_loop_speed.isnumeric()) and 1 <= color_loop_speed <= 255:
        request_data["colorloopspeed"] = int(color_loop_speed)
    elif color_loop_speed is not None:
        errors += ["color_loop_speed"]

    if ct is not None and (isinstance(ct, int) or isinstance(ct, str) and ct.isnumeric()):
        request_data["ct"] = int(ct)
    elif ct is not None:
        errors += ["ct"]

    if effect is not None and effect in ["none", "colorloop"]:
        request_data["effect"] = effect
    elif effect is not None:
        errors += ["effect"]

    if hue is not None and (
            isinstance(hue, int) or isinstance(hue, str) and hue.isnumeric()) and 0 <= hue <= 65535:
        request_data["hue"] = int(hue)
    elif hue is not None:
        errors += ["hue"]

    print("on the air", on)
    if on is not None and (
            isinstance(on, bool) or isinstance(on, str) and on in ["true", "True", "false", "False"]):
        if isinstance(on, str) and on in ["False", "false"]:
            request_data["on"] = bool(0)
        else:
            request_data["on"] = bool(on)
    elif on is not None:
        errors += ["on"]

    if saturation is not None and (isinstance(saturation, int) or isinstance(saturation,
                                                                             str) and saturation.isnumeric()) and 0 <= saturation <= 255:
        request_data["sat"] = int(saturation)
    elif saturation is not None:
        errors += ["saturation"]

    if transition_time is not None and (
            isinstance(transition_time, int) or isinstance(transition_time, str) and transition_time.isnumeric()):
        request_data["transitiontime"] = int(transition_time)
    elif transition_time is not None:
        errors += ["transition_time"]

    if x is not None and y is not None and (
            isinstance(x, float) or isinstance(x, str) and x.replace(".", "", 1).isdigit()) and (isinstance(y,
                                                                                                            float) or isinstance(
        y, str) and y.replace(".", "", 1).isdigit()) and 0 <= x <= 1 and 0 <= y <= 1:
        request_data["xy"] = [float(x), float(y)]
    elif x is not None or y is not None:
        errors += ["xy"]

    return {"error": errors, "request_data": request_data}


def get_device_data_from_deconz(device_id, username=None):
    if device_id == -1:
        if not TEST:
            response_tmp = deconz_api.get_all_lights()
        else:
            response_tmp = {
                "1": {
                    "etag": "026bcfe544ad76c7534e5ca8ed39047c",
                    "hascolor": True,
                    "manufacturer": "dresden elektronik",
                    "modelid": "FLS-PP3",
                    "name": "Light 1",
                    "pointsymbol": {},
                    "state": {
                        "alert": "none",
                        "bri": 111,
                        "colormode": "ct",
                        "ct": 307,
                        "effect": "none",
                        "hue": 7998,
                        "on": True,
                        "reachable": True,
                        "sat": 172,
                        "xy": [0.421253, 0.39921]
                    },
                    "swversion": "020C.201000A0",
                    "type": "Extended color light",
                    "uniqueid": "00:21:2E:FF:FF:00:73:9F-0A"
                },

                "2": {
                    "etag": "026bcfe544ad76c7534e5ca8ed39047c",
                    "hascolor": False,
                    "manufacturer": "dresden elektronik",
                    "modelid": "FLS-PP3 White",
                    "name": "Light 2",
                    "pointsymbol": {},
                    "state": {
                        "alert": "none",
                        "bri": 1,
                        "effect": "none",
                        "on": False,
                        "reachable": True
                    },
                    "swversion": "020C.201000A0",
                    "type": "Dimmable light",
                    "uniqueid": "00:21:2E:FF:FF:00:73:9F-0B"
                }
            }

        response = []
        for key, value in response_tmp.items():
            response += [format_device_data_from_deconz(key, value)]

        return response
    else:
        response = deconz_api.get_light_state(device_id)
        response = format_device_data_from_deconz(device_id, response)

        return response


def update_light_state_deconz(device_id, alert=None, brightness=None, color_loop_speed=None, ct=None, effect=None,
                              hue=None, on=None,
                              saturation=None, transition_time=None, x=None, y=None):
    zwErg = format_light_attributes_for_deconz(alert, brightness, color_loop_speed, ct, effect, hue, on, saturation,
                                               transition_time, x, y)
    print("cool", zwErg["request_data"])
    response = deconz_api.update_light_state(device_id.__str__(), zwErg["request_data"])

    return {"error": zwErg["error"], "response": response}
