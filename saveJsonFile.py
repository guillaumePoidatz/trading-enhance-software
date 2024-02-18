import json

def saveJsonFile(data,fileName):

    with open(fileName, 'w') as outfile:
        json.dump(data, outfile, indent=0)

    return None
