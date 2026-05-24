import random
import string

import requests

from data import PASSWORD, USER_NAME
from urls import INGREDIENTS_API, ORDERS_API, REGISTER_USER_API, USER_API


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ""
    for _ in range(length):
        random_string = random_string + random.choice(letters)
    return random_string


def get_user_data():
    unique_part = generate_random_string(10)
    return {
        "email": f"{unique_part}@example.com",
        "password": PASSWORD,
        "name": USER_NAME,
    }


def create_user(payload):
    response = requests.post(REGISTER_USER_API, json=payload)
    response.raise_for_status()
    return response


def delete_user(token):
    return requests.delete(USER_API, headers={"Authorization": token})


def get_ingredient_ids(count=2):
    response = requests.get(INGREDIENTS_API)
    response.raise_for_status()
    return [ingredient["_id"] for ingredient in response.json()["data"][:count]]


def create_order(token, ingredient_ids):
    payload = {"ingredients": ingredient_ids}
    response = requests.post(ORDERS_API, json=payload, headers={"Authorization": token})
    response.raise_for_status()
    return response


def normalize_order_number(order_number):
    return str(order_number).lstrip("0") or "0"


def order_number_variants(order_number):
    normalized = normalize_order_number(order_number)
    padded5 = normalized.zfill(5)
    padded6 = normalized.zfill(6)
    return {
        normalized,
        padded5,
        padded6,
        f"#{normalized}",
        f"#{padded5}",
        f"#{padded6}",
    }
