import requests
from jdict import jdict

# data = requests.get('https://api.anonfiles.com/v2/file/n2weifEcx5/info')
# json_data = data.json()
# print(type(json_data))


json_data = {
    "status": True,
    "data": {
        "file": {
            "url": {
                "short": "https://anonfiles.com/n2weifEcx5",
                "full": "https://anonfiles.com/n2weifEcx5/test_py",
            },
            "metadata": {
                "size": {"bytes": 63, "readable": "63 B"},
                "name": "test_py",
                "id": "n2weifEcx5",
            },
        }
    },
}

new_data = jdict(json_data)


for key, value in new_data.data.file.metadata.items():
    print(key, value)
