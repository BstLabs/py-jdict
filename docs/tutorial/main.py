import requests
import jdict
import json

from subprocess import run
from os import environ, path

def _upload_file() -> str:
    cwd = path.dirname(__file__)
    environ["PATH"] = f'{environ["PATH"]}:{cwd}'
    cmd = 'curl -F "file=@test.txt" https://api.anonfiles.com/upload'
    result = run(cmd, capture_output=True, env=environ, text=True, check=True, shell=True)
    result_dict = json.loads(result.stdout)
    return result_dict['data']['file']['metadata']['id']

def _get_file_info() -> dict:
    url = f"https://api.anonfiles.com/v2/file/{_upload_file()}/info"
    return requests.get(url).json()

def _apply_jdict() -> jdict.jdict:
    file = _get_file_info()
    jdict.set_codec()
    return jdict.jdict(file)

data = _apply_jdict()
print(type(data))
print(data.data.keys())
print(data.data.file)