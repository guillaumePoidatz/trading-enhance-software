import json


def read_json_file(fileName):
    with open(fileName) as f:
        data = json.load(f)

    return data


def save_json_file(data, fileName):
    with open(fileName, "w") as outfile:
        json.dump(data, outfile, indent=0)

    return None
