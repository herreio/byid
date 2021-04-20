import csv
import json
import time
import ijson
import requests
import xmltodict
from tqdm import tqdm
from timeit import default_timer as timer


# ////////////// #
# /// CSV IO /// #
# ////////////// #


def write_csv(path_to_file, csv_file_data):
    with open(path_to_file, "w", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writerows(csv_file_data)


# /////////////// #
# /// JSON IO /// #
# /////////////// #


def read_json(path_to_file):
    with open(path_to_file) as f:
        return json.load(f)


def read_json_stream(path_to_file):
    contents = {}
    with open(path_to_file) as f:
        items = ijson.kvitems(f, "")
        for k, v in tqdm(items):
            contents[k] = v
    return contents


def write_json(path_to_file, json_file_data):
    with open(path_to_file, "w") as f:
        json.dump(json_file_data, f, ensure_ascii=False, indent=2)


# //////////////// #
# /// HTTP GET /// #
# //////////////// #


def fetch_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            print("URL", url)
            print("HTTP", response.status_code)
            return None
    except Exception as e:
        print("request to", url, "failed!")
        print(e)
        return None


def fetch_text(url):
    response = fetch_url(url)
    if response:
        return response.text
    return ""


def fetch_json(url):
    response = fetch_url(url)
    if response:
        return response.json()
    return {}


def fetch_xml(url):
    response_text = fetch_text(url)
    if response_text:
        payload = xmltodict.parse(response_text)
        return json.loads(json.dumps(payload))
    return {}


def cursor(dois, func, *args, **kwargs):
    pages = {}
    for doi in tqdm(dois):
        response = func(doi, *args, **kwargs)
        if response:
            pages[doi] = response
    return pages


def cursor_limited(dois, func, quota, *args, **kwargs):
    pages = {}
    rate = quota["sec"] / quota["max"]
    for doi in tqdm(dois):
        start = timer()
        response = func(doi, *args, **kwargs)
        if response:
            pages[doi] = response
        margin = rate - (timer() - start)
        if margin > 0:
            time.sleep(margin)
    return pages
