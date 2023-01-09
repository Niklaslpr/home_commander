import re

from django.shortcuts import render
import urllib.parse

DECONZ_URL = "http://192.168.178.49"
API_KEY = "546117A96A"
TEST = True  # @Niklas set it to False


def get_data_from_input(data_input):
    # print("data_input", urllib.parse.unquote(data_input.read().decode("utf-8")))
    # print("is that magic", chr(int("0x5B", 16)))

    # test_string = data_input.read().decode("utf-8")
    # print("testString", test_string)
    # for x in data_input.read().decode("utf-8").split("&"):
    #     print("x", x)
    raw_data = urllib.parse.unquote(data_input.body.decode("utf-8"))

    print("raw data", raw_data)

    data = {}

    if raw_data != "":
        for entry in raw_data.split("&"):
            if re.search(r"^\w+\[\w+]=\w+$", entry):
                print("it goes here", entry)
                parent = entry.split("[")[0]
                child = entry.split("[")[1].split("]")[0]
                value = entry.split("[")[1].split("]")[1][1:]

                print("parent", parent)
                print("child", child)
                print("value", value)

                if parent not in data.keys():
                    data[parent] = {}
                data[parent][child] = value
            else:
                print("nope here", entry)
                data[entry.split("=")[0]] = entry.split("=")[1]

    return data


def home(response):
    return render(response, "main/home.html", {})
