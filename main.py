"""
Brief:
GET /products/:category – Return a listing of products in a given category.
GET /availability/:manufacturer – Return a list of availability info.
The APIs are running at https://bad-api-assignment.reaktor.com/.

By Aditya Kelekar
"""
import time
import re

import json
import requests
from flask import Flask
from flask import redirect, render_template, request

app = Flask(__name__)

headers = {"x-force-error-mode": "all"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/acce")
def acce():
    accessories = "https://bad-api-assignment.reaktor.com/products/accessories"
    id_dict = fetch_info(accessories)
    return render_template("acce.html", main_info=id_dict)


@app.route("/shirts")
def shirts():
    shirts = "https://bad-api-assignment.reaktor.com/products/shirts"
    id_dict = fetch_info(shirts)
    return render_template("shirts.html", main_info=id_dict)


@app.route("/jackets")
def jackets():
    jackets = "https://bad-api-assignment.reaktor.com/products/jackets"
    id_dict = fetch_info(jackets)
    return render_template("jackets.html", main_info=id_dict)


def find_manuf_name(api, id):
    """
    Takes a product id and API for the availability data
    Returns availability data for a particular product
    """
    MAX_TRIES = 3
    tries = 0
    while True:
        response = requests.get(api)
        if response.status_code == 500 and tries < MAX_TRIES:
            tries += 1
            continue
        break

    response_str = response.json()
    info = response_str["response"]
    print(id)
    return info


def fetch_info(product):
    t0 = time.time()
    api_address = product
    MAX_TRIES = 3
    tries = 0
    response = None
    headers = {"x-force-error-mode": "all"}

    while True:
        response = requests.get(api_address, headers=headers)
        if response.status_code == 500 and tries < MAX_TRIES:
            tries += 1
            continue
        break
    response_str = response.json()

    id_dict = (
        {}
    )  # id_dict is a dict with keys: product ids   and    values: list containing product info
    availability_info_dict = {}

    for a in response_str:
        current_id = a["id"]
        current_name = a["name"]
        a_price = a["price"]
        a_manufacturer = a["manufacturer"]
        a_colors = [somecolor for somecolor in a["color"]]

        id_dict[current_id] = ["name: " + current_name]
        id_dict[current_id].append("price: " + str(a_price))
        id_dict[current_id].append("manufacturer: " + a_manufacturer)
        id_dict[current_id].append("colors: " + ", ".join(a_colors))

        api_address_manuf = "https://bad-api-assignment.reaktor.com/availability/"
        manufacturer = a["manufacturer"]
        api_address_manuf += manufacturer
        current_id_upper = current_id.upper()

        # if manufacturer already encountered earlier
        if manufacturer in availability_info_dict.keys():
            for a in availability_info_dict[manufacturer]:
                current_id_new = a["id"]
                if current_id_new == current_id_upper:
                    availability_big_string = a["DATAPAYLOAD"]
                    break
            availability_temp_string = re.search(
                "<INSTOCKVALUE>(.*)</INSTOCKVALUE>", availability_big_string
            )
            availability_small_string = availability_temp_string.group(1)
            id_dict[current_id].append("availability: " + availability_small_string)

        else:
            availability_info = find_manuf_name(api_address_manuf, current_id_upper)
            for a in availability_info:
                current_id_new = a["id"]
                if current_id_new == current_id_upper:
                    availability_big_string = a["DATAPAYLOAD"]
                    break
            availability_temp_string = re.search(
                "<INSTOCKVALUE>(.*)</INSTOCKVALUE>", availability_big_string
            )
            availability_small_string = availability_temp_string.group(1)
            id_dict[current_id].append("availability: " + availability_small_string)

            availability_info_dict[
                manufacturer
            ] = availability_info  # add "availability_info" to availability_info_dict

    t1 = time.time()
    nsec = t0 - t1
    print(nsec)

    return id_dict

if __name__ == "__main__":
    app.server(host="0.0.0.0", port=8080, debug=True)
