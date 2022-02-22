# JDICT

JavaScript-like Python dictionary. 
For background and design description look at this [Medium article](https://medium.com/swlh/jdict-javascript-dict-in-python-e7a5383939ab).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `jdict` from the PyPi site:

```bash
pip3 install pyjdict
```

## What is jdict?

Let's imagine we have some deeply nested json structure as following(okay this is not deeply nested, but it is okay):

```json
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
```

Now, you need get the `id` of this data, yes you are going to feel the pain as: `this_awesome_json["data"]["file"]["metadata"]["id"]`.

But how about accessing this id as: `this_awesome_json.data.file.metadata.id`? Even for loop and assign values directly using .[dot] access?

That's where the jdict shines. It is lightweight, nearly zero cost library converts your dictionaries to special jdict type and you are ready to go.

## Usage

Now let's build small script to show the jdict. We are going to use anonymous file upload public API.

```py
import requests
import json
from pyjdict import jdict, set_codec

# Send post request and upload the test.txt file - you can create one
def _upload_file() -> str:
    file = {"file": open("test.txt", "rb")}
    result = requests.post("https://api.anonfiles.com/upload", files=file)
    result_dict = result.json()
    # Feel the pain here
    return result_dict["data"]["file"]["metadata"]["id"]

# Send get request and get back the json information about the uploaded file
def _get_file_info() -> dict:
    url = f"https://api.anonfiles.com/v2/file/{_upload_file()}/info"
    return requests.get(url).json()

# Change codec to use jdict
def _convert_to_jdict() -> jdict:
    set_codec(json)
    return _get_file_info()
```

The killer point here is to change the codec and then convert our dictionary to jdict.

If you are using [simplejson](https://pypi.org/project/simplejson/), just pass it as `pyjdict.set_codec(simplejson)`, it will do the same trick.

Great, now we are ready to use it:

```py
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
    # Set the id:
    data.data.file.metadata.id = "MYID"
    print("ID: ", data.data.file.metadata.id)

```

Sample output:

```sh
$ python3 main.py

ID:  h8p2SbGfx2
size {'bytes': 19, 'readable': '19 B'}
name test_txt
id h8p2SbGfx2
ID:  MYID
```

## Patching

The next crucial feature is to ability to path core libraries with jdict.

Just think about the boto3 library, with AWS you may encounter really deeply nested json structures, 
with jdict you can access those nested values with `.[dot]` notation as well.

By patching `botocore.parsers` you gain really powerful tooling to work with:

```py
import os
import boto3
import pyjdict

pyjdict.patch_module('botocore.parsers')

def test_library():
    response = boto3.client('s3').list_buckets()
    assert(response.Buckets == response['Buckets'])
    return 'OK'
```

> Just keep in mind that you need to have valid AWS credentials to run this code


## License

MIT License, Copyright (c) 2021-2022 BST LABS. See [LICENSE](LICENSE.md) file.




