import requests
import json
from pyjdict import jdict, set_codec


def _upload_file() -> str:
    file = {"file": open("test.txt", "rb")}
    result = requests.post("https://api.anonfiles.com/upload", files=file)
    result_dict = result.json()
    # Feel the pain here
    return result_dict["data"]["file"]["metadata"]["id"]


def _get_file_info() -> dict:
    url = f"https://api.anonfiles.com/v2/file/{_upload_file()}/info"
    return requests.get(url).json()


def _convert_to_jdict() -> jdict:
    set_codec(json)
    return _get_file_info()


if __name__ == "__main__":
    """
    Sample data:
    {
        "status": True,
        "data": {
            "file": {
                "url": {
                    "short": "https://anonfiles.com/t3l5S2Gex3",
                    "full": "https://anonfiles.com/t3l5S2Gex3/test_txt",
                },
                "metadata": {
                    "size": {"bytes": 19, "readable": "19 B"},
                    "name": "test_txt",
                    "id": "t3l5S2Gex3",
                },
            }
        },
    }
    """
    data = _convert_to_jdict()
    # Get the id:
    print("ID: ", data.data.file.metadata.id)
    # Use in for loop:
    for key, value in data.data.file.metadata.items():
        print(key, value)
    # Assign values easily:
    data.data.file.metadata.id = "MYID"
    print("ID: ", data.data.file.metadata.id)