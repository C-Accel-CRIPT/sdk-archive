"""
Running this file will update the .json key files.

"""
import pathlib
import json

import cript


def save_keys(api):
    for key, value in api.keys.items():
        with open("key_" + key + ".json", "w", encoding="UTF-8") as f:
            json.dump(value, f, sort_keys=True, indent=4)


def main():
    host = "criptapp.org"
    with open(str(pathlib.Path(__file__).parent.parent.parent.parent) + "\\api_key.txt", "r") as f:
        token = f.read()
    api = cript.API(host, token)
    save_keys(api)


if __name__ == "__main__":
    main()
