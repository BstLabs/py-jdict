import requests
from box import Box

data = requests.get('https://api.anonfiles.com/v2/file/n2weifEcx5/info')
json_data = data.json()

new_data = Box(json_data)

for key, value in new_data.data.file.metadata.items():
    print(key, value)
