from django.shortcuts import render

DECONZ_URL = "http://192.168.178.49"
API_KEY = "546117A96A"
TEST = True  # @Niklas set it to False


def get_data_from_input(data_input):
    return {entry.split("=")[0]: entry.split("=")[1] for entry in
            data_input.read().decode("utf-8").split("&")} if data_input.read().decode("utf-8") != "" else {}


def home(response):
    return render(response, "main/home.html", {})
