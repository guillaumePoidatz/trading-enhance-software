import json

def readJsonFile(fileName):
    with open(fileName) as f:
        data = json.load(f)

    return data
